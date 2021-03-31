
metajson = {'estimators': [] }

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':0.01, 'max_iter':1000}, 
    'kind':'classifier', 'name': 'logreg0.01'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':0.1, 'max_iter':1000}, 
    'kind':'classifier', 'name': 'logreg0.1'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':1, 'max_iter':1000}, 
    'kind':'classifier','name': 'logreg1'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':10, 'max_iter':1000}, 
    'kind':'classifier','name': 'logreg10'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':100, 'max_iter':1000}, 
    'kind':'classifier','name': 'logreg100'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':1000, 'max_iter':1000}, 
    'kind':'classifier','name': 'logreg1000'})

metajson['estimators'].append({'estimator':'LogisticRegression', 
     'kwargs':{'penalty':'l2', 'solver':'lbfgs', 'C':10000, 'max_iter':1000}, 
    'kind':'classifier','name': 'logreg10000'})

metajson['estimators'].append({'estimator':'LinearRegression', 
     'kwargs':{}, 
    'kind':'regressor','name': 'linreg'})

metajson['estimators'].append({'estimator':'BernoulliNB', 
     'kwargs':{}, 
    'kind':'classifier','name': 'bernoullinb'})

metajson['estimators'].append({'estimator':'AdaBoostClassifier', 
     'kwargs':{'n_estimators':30}, 
    'kind':'classifier','name': 'adaboost30'})

metajson['estimators'].append({'estimator':'AdaBoostClassifier', 
     'kwargs':{'n_estimators':100}, 
    'kind':'classifier','name': 'adaboost100'})

metajson['estimators'].append({'estimator':'AdaBoostClassifier', 
     'kwargs':{'n_estimators':300}, 
    'kind':'classifier','name': 'adaboost300'})


metajson['estimators'].append({'estimator':'RandomForestClassifier', 
     'kwargs':{'n_estimators':300}, 
    'kind':'classifier','name': 'rfc300'})

metajson['estimators'].append({'estimator':'RandomForestClassifier', 
     'kwargs':{'n_estimators':1000}, 
    'kind':'classifier','name': 'rfc1000'})

metajson['estimators'].append({'estimator':'RandomForestClassifier', 
     'kwargs':{'n_estimators':1000}, 
    'kind':'classifier','name': 'rfc3000'})


metajson['estimators'].append({'estimator':'SVC', 
     'kwargs':{'C':1}, 
    'kind':'classifier','name': 'svc1'})


metajson['estimators'].append({'estimator':'Ridge', 
     'kwargs':{}, 
    'kind':'regressor','name': 'ridge'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.0001}, 
    'kind':'classifier','name': 'sgdc0'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.001}, 
    'kind':'classifier','name': 'sgdc1'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.01}, 
    'kind':'classifier','name': 'sgdc2'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.00001}, 
    'kind':'classifier','name': 'sgdc3'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.0001, 'penalty':'l1'}, 
    'kind':'classifier','name': 'sgdc4'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.0001, 'penalty':'elasticnet'}, 
    'kind':'classifier','name': 'sgdc5'})

metajson['estimators'].append({'estimator':'SGDClassifier', 
     'kwargs':{'alpha':0.00001, 'penalty':'elasticnet'}, 
    'kind':'classifier','name': 'sgdc6'})




import json
with open('../processed_data/evaluation_estimators.json', 'w') as f:
    json.dump(metajson, f,indent=1, sort_keys=True)
