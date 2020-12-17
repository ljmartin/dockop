import altair as alt
from scipy.stats import bayes_mvs
from sklearn.metrics import average_precision_score
import h5py
from scipy.special import logit, expit
import pandas as pd
import numpy as np

import json
json_name = '../processed_data/evaluation_estimators.json'
estimators = json.load(open(json_name, 'r'))['estimators']

true_scores = np.load('../processed_data/AmpC_short.npy')




fps = ['morgan', 'morgan_feat', 'atompair', 'topologicaltorsion','pattern', 'rdk']

results_df = pd.DataFrame(columns=['Fingerprint', 'Average Precision', 
                                   'low_ap', 'high_ap', 
                                   'FPSize', 'Estimator'])


def evaluate(x, fp):
    results_df = pd.DataFrame(columns=['Fingerprint', 'Average Precision', 
                                       'low_ap', 'high_ap',
                                       'FPSize','Estimator'])
    count=0
    for size in x:
        f = h5py.File('../processed_data/'+fp+'_'+str(size)+'_'+'15000_'+estimator_name+'.hdf5', 'r')
        nranks = list()
        aps= list()
        for _ in range(5):
            proba = f[f'repeat{_}']['prediction'][:].copy()
            test_idx = f[f'repeat{_}']['test_idx'][:].copy()[~np.isinf(proba)]
            
            aps.append(average_precision_score(true_scores[test_idx]<-60, 
                                                                 proba[~np.isinf(proba)]))
            
        mean = expit(np.mean(logit(aps)))
        cr = bayes_mvs(logit(aps))[0][1]
        f.close()
        
        results_df.loc[count] = [fp, mean, expit(cr[0]), expit(cr[1]), size, estimator_name]
        count+=1
    return results_df

for fp in fps:
    for estimator in estimators:
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

# generate the error bars
errorbars = alt.Chart().mark_errorbar().encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False),
           axis=alt.Axis(labelAngle=60)),
    y=alt.Y("low_ap:Q", title='Average Precision'),
    y2="high_ap:Q",
    color=alt.Color('Estimator')
)

lines = alt.Chart().mark_line(size=3).encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False)),
    y=alt.Y('Average Precision', ),
    color=alt.Color('Estimator'),
    
)

points = alt.Chart().mark_point(size=60, filled=True).encode(
    x=alt.X('FPSize', scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False)),
    y=alt.Y('Average Precision', ),
    color=alt.Color('Estimator'),
    
)

hline = alt.Chart().mark_rule(size=1, strokeDash=[10, 10]).encode(
    y=alt.Y('a:Q'),
)

ch =alt.layer(
    hline,
    errorbars, 
    lines, 
    points, 
#    hline,
    data=results_df
).transform_calculate(
    a="0.013"
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

ch.save('../processed_data/fpsize_figure.html')
