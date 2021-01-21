import altair as alt
from scipy.stats import bayes_mvs
from sklearn.metrics import average_precision_score
import h5py
from scipy.special import logit, expit
import pandas as pd
import numpy as np

import json
json_name = '../../processed_data/evaluation_estimators.json'
estimators = json.load(open(json_name, 'r'))['estimators']

true_scores = np.load('../../processed_data/AmpC_short.npy')




fps = ['morgan', 'morgan_feat', 'atompair', 'topologicaltorsion','pattern', 'rdk']
fps = ['morgan', 'morgan_feat']

results_df = pd.DataFrame(columns=['Fingerprint', 'Average Precision', 
                                   'FPSize', 'Estimator'])


def evaluate(x, fp):
    results_df = pd.DataFrame(columns=['Fingerprint', 'Average Precision',
                                       'FPSize','Estimator'])
    count=0
    for size in x:
        f = h5py.File('../../processed_data/'+fp+'_'+str(size)+'_'+'25000_'+estimator_name+'.hdf5', 'r')
        nranks = list()
        aps= list()
        for _ in range(5):
            proba = f[f'repeat{_}']['prediction'][:].copy()
            test_idx = f[f'repeat{_}']['test_idx'][:].copy()[~np.isinf(proba)]

            cutoff = np.percentile(true_scores[test_idx], 0.05)
            
            ap = average_precision_score(true_scores[test_idx]<cutoff, 
                                                                 proba[~np.isinf(proba)])
            results_df.loc[count] = [fp, ap, size, estimator_name]
            count+=1
            
        f.close()
        
    return results_df

for fp in fps:
    for estimator in estimators:
        if estimator['name']=='linreg':
            continue
        print(fp, estimator['name'])
        estimator_name = estimator['name']

        if fp=='maccs':
            x = [83,166]
        else:
            x=  [64<<i for i in range(1,11)]
        
        df = evaluate(x, fp)
    
        results_df = pd.concat([results_df, df])




low = 32
high = 70000 #65536

highest_ap = df.groupby(['Fingerprint', 'FPSize', 'Estimator']).mean('Average Precision').max()['Average Precision']
#highest_ap = results_df['Average Precision'].max()

# generate the error bars
errorbars = alt.Chart().mark_errorbar(extent='ci').encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False),
           axis=alt.Axis(labelAngle=60)),
    y=alt.Y("Average Precision", title='Average Precision'),
    color=alt.Color('Estimator')
)

lines = alt.Chart().mark_line(size=3).encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False)),
    y=alt.Y('Average Precision', aggregate='mean'),
    color=alt.Color('Estimator'),
    
)

points = alt.Chart().mark_point(size=60, filled=True).encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False)),
    y=alt.Y('Average Precision', aggregate='mean'),
    color=alt.Color('Estimator'),
    
)

hline = alt.Chart().mark_rule(size=1, strokeDash=[10, 10]).encode(
    y=alt.Y('a:Q'),
)

maxline = alt.Chart().mark_rule(size=0.5).encode(
    y=alt.Y('b:Q'),
)

ch =alt.layer(
    hline,
    maxline,
    errorbars, 
    lines,
    points, 

    data=results_df
).transform_calculate(
    a="0.004",#random clf average precision is equal to the rate of occurrence, 4th percentile or 0.004
    b=str(highest_ap)
).properties(width=350, height=250, ).facet(
    #'Fingerprint', columns=2
    facet=alt.Facet('Fingerprint',header=alt.Header(labelFontSize=15),),
    
    #header=alt.Header(labelFontSize=25),
    #column=alt.Column(field=alt.Field('Fingerprint'),type='nominal'),
    columns=2
).configure_axis(
   #labelFontSize=10,
   #titleFontSize=15
).configure_header(titleFontSize=15,)

ch.resolve_scale(x='independent').save('../../figures/fpsize_figure.html')
