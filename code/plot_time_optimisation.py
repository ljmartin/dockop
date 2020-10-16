import json
from set_up import Setup

import h5py
from scipy.special import logit
import pandas as pd
from scipy.special import expit
import pymc3 as pm
import numpy as np


true_scores = np.load('../processed_data/AmpC_short.npy')

setup = Setup('morgan', '../processed_data/AmpC', verbose=True)
setup.load_scores()
true_hit_rate = (setup.scores<-60).sum() / setup.scores.shape[0]
num_true_hits = (setup.scores<-60).sum()

possible_sizes = np.geomspace(300, 150000, 20).astype(int)
json_name = '../processed_data/logreg_only.json'
estimators = json.load(open(json_name, 'r'))['estimators']



def load_results(trainingSetSize):
    """Just loads the hdf file from ../processed_data.
    This scrip only uses morgan fingerprint and size 4096"""
    fptype = 'morgan'
    fpSize = 4096
    estimator_name = 'logreg0.1'

    f = h5py.File('../processed_data/'+fptype+'_'+str(fpSize)+'_'+str(trainingSetSize)+'_'+estimator_name+'.hdf5', 'r')
    nranks = list()
    for _ in range(5):
        proba = f[f'repeat{_}']['prediction'][:].copy()
        ranked_predictions = (-proba[~np.isinf(proba)]).argsort().argsort()
        test_idx = f[f'repeat{_}']['test_idx'][:].copy()[~np.isinf(proba)]
        normalized_ranks = (1+ranked_predictions[true_scores[test_idx]<-60]) / (len(test_idx)+1)
        nranks.append(normalized_ranks)
    f.close()
    
    return nranks


def estimate_student(normalized_ranks):
    """This fits a PyMC3 model. All the model does is
    fit the parameters for t distribution, since it is clear
    (in the authors opinion) that the logit-transformed ranks 
    are very well described by a t distribution. The logit
    ranks are thus the observations, and the model finds the 
    ranges of parameters consistent with those obs."""

    with pm.Model() as model:
        nu = pm.HalfNormal('nu', 50) #very broad priors
        mu = pm.Normal('mu', mu=0, sigma=50) #very broad priors
        sigma = pm.HalfNormal('sig', 50) #very broad priors
    
        lik = pm.StudentT('t', nu=nu,mu=mu, sigma=sigma, observed=logit(normalized_ranks))
        trace = pm.sample(1000, tune=1000)
    return trace, model


#########
#####Run through the training sizes used, and
#####send it to pymc3 to estimate parameters of the
#####logit-transformed ranks.
#####Time est. 20minutes.
#########

normalized_ranks_holder = list()
estimate_holder = list()

for size in possible_sizes:
    normalized_ranks = load_results(size)
    normalized_ranks_holder.append(normalized_ranks)
    
    
    nuts_trace = estimate_student(np.concatenate(normalized_ranks))
    estimate_holder.append(nuts_trace)
    


#########
######Run through some simulations of a docking campaign. 
######We ask the model to find a desired number of hits (score <-60).
######Assuming we know the hit rate in the dataset, we only
######need to pull a set number of ligands from a virtual library.'
######Then, we expect to find, say, 50% of those hits, leaving the
######other 50% undiscovered. Using these numbers, we can calculate
######how many ligands to pull, and based on a range of training set sizes
######can estimate how much actual docking time would be spent getting
######to the target number. 
#########

df = pd.DataFrame(columns=['Computation days (single core)', 'low', 'high', 
                               'Train set size', 'Desired number of ligands'])

count = 0

sample_num_hits = (setup.scores<-60).sum()    
sample_hit_rate = sample_num_hits / setup.scores.shape[0]
training_set_sizes = np.geomspace(300, 150000, 20).astype(int)
percentage = 0.5

for desired_num_hits in np.linspace(10000,300000,11):
    
    n_hits_pulled = desired_num_hits / percentage
    n_ligands_to_pull = n_hits_pulled / sample_hit_rate 
    
    for idx, size in enumerate(training_set_sizes):
        num_already_found = np.mean([sample_num_hits - i.shape[0] for i in normalized_ranks_holder[idx]])
        
        num_remaining = n_hits_pulled - num_already_found
        num_needed =  desired_num_hits-num_already_found
        fraction_required = num_needed / num_remaining
        
        #expected performance on undocked ligands:
        trace = estimate_holder[idx][0]
        mu = trace['mu']
        nu = trace['nu']
        sig = trace['sig']
        samples = t(nu,mu,sig).ppf(fraction_required)
        
        #this is the fraction of remaining ligands we need to dock to reach the goal. 
        hpd = expit(pm.hpd(samples))
    
        time_hpd = hpd * (n_ligands_to_pull - size) + size
        time_days = time_hpd / 60 / 60 /24
        time_mean = expit(samples.mean())*(n_ligands_to_pull - size) + size
        time_mean = time_mean/60/60/24
        
        print(time_mean)
        
        df.loc[count] = [time_mean, time[0], time[1], size, desired_num_hits]
        count+=1


import altair as alt
#now plot :)
line = alt.Chart(df).mark_line(size=3).encode(
    x = alt.X('Train set size:Q',title='Training set size'),
    y = alt.Y('Computation days (single core):Q', title=['Computation days', '(single core)'],
             scale=alt.Scale(type='log',base=10,zero=False)),
         #scale=alt.Scale(type='log',base=2, domain=(1,100),zero=False)
    color = alt.Color('Desired number of ligands:O', title=['Desired number', 'of ligands'], )
)
line.save('../processed_data/time_comparison.html')
