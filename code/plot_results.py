from sklearn.metrics import average_precision_score
import pandas as pd
import h5py
from scipy.special import logit, expit
from scipy.stats import bayes_mvs
import numpy as np
import altair as alt



import json
true_scores = np.load('../processed_data/AmpC_short.npy')
json_name = '../processed_data/evaluation_estimators.json'
estimators = json.load(open(json_name, 'r'))['estimators']




df = pd.DataFrame(columns=['Fingerprint', 'Algorithm', 'mean', 'low_cr', 'high_cr'])
namedict = dict()
namedict['maccs'] = 'MACCS'
namedict['morgan'] = 'Morgan'
namedict['topologicaltorsion'] = 'Topological\nTorsion'
namedict['atompair'] = 'Atom\nPair'
namedict['pattern'] = 'Pattern'

algodict=dict()
algodict['logreg1'] = 'Logistic Regression'
algodict['rfc3000'] = 'Random Forest'
algodict['svc1'] = 'Support Vector Classifier'

count = 0


for fp,size in zip(['maccs', 'morgan', 'topologicaltorsion', 'atompair', 'pattern'],
                   [168, 256, 256, 256, 256]):
    for estimator in estimators[:]:
        if estimator['name'] in ['logreg1', 'rfc3000', 'svc1']:
            pass
        else:
            continue

        f = h5py.File('../processed_data/'+fp+'_'+str(size)+'_'+estimator['name']+'.hdf5', 'r')
        nranks = list()
        aps= list()
        for _ in range(5):
            proba = f[f'repeat{_}']['prediction'][:].copy()
            test_idx = f[f'repeat{_}']['test_idx'][:].copy()[~np.isinf(proba)]
            
            aps.append(average_precision_score(true_scores[test_idx]<-60, 
                                                                 proba[~np.isinf(proba)]))
            
        mean = expit(np.mean(logit(aps)))
        cr = bayes_mvs(logit(aps))[0][1]
        print(fp, estimator['name'], expit(cr))

        f.close()
        df.loc[count] = [namedict[fp], algodict[estimator['name']], mean, expit(cr[0]), expit(cr[1])]
        count+=1



points = alt.Chart().mark_point(filled=True).encode(
    alt.X(
        'mean:Q',
        title="Average Precision",

        axis=alt.Axis(grid=False)
    ),
    alt.Y(
        'Algorithm:N',
        title="",
        sort='-x',
        axis=alt.Axis(grid=True)
    ),
    color = alt.Color('Algorithm')
)

error_bars = points.mark_rule().encode(
    x='low_cr',
    x2='high_cr',
)


line = alt.Chart().mark_rule().encode(
    x='a:Q',
)

ch= alt.layer(points,error_bars,line,  data=df).transform_calculate(
    a="0.013"
).facet(row='Fingerprint')
ch.save('../processed_data/initial_run.html')
