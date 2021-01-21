from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC, SVR, LinearSVC
from sklearn.gaussian_process import GaussianProcessClassifier

import time
import numpy as np
from scipy.special import logit


class CommonEstimator(object):
    """ This class just provides a common interface for both classifiers and regressors.
    Makes things easier in the evaluation stage, I can just iterate through estimator:parameter 
    pairs from a JSON and it will work."""
    def __init__(self, parameters, cutoff=1.0, verbose=False):
        """
        Instantiate this with a set of hyperparameters to get an sklearn estimator object 
        with fit and predict methods that will work for both classifiers and regressors.
        In my case, the goal is ranking so the predict method for classifiers is actually
        `predict_proba`
        
        
        Parameters:
        -----------
        parameters: dict:
            - 'kwargs': dict. hyperparameters for a sklearn estimator. 
            - 'estimator': str. the name of an sklearn estimator, i.e.
                `LogisticRegression` or `LinearRegression`.
            - 'kind': str. one of `classifier` or `regressor`
        """
        self.cutoff = cutoff
        #these are the hyperparameters:
        self.kwargs = parameters['kwargs']

        #instantiate an estimator from a string (i.e. "LogisticRegression")
        #and feed it the hyperpararmeters
        ##WARNING: eval is typically not used due to security issues of loading and
        ##executing unknown code. In this case, however, I control the contents of
        ##the JSON file in my own repo. 
        self.estimator = eval(parameters['estimator'])(**self.kwargs)
                
        #this helps later when fitting.
        self.kind = parameters['kind']

        self.verbose = verbose
        
    def fit(self, X, y):
        """Got to binarize the `y` labels in the case of a classifier."""
        if self.verbose:
            start = time.time()

            
            cutoff = np.percentile(y, self.cutoff) #estimate the percentile cutoff from the training set.
            #(this is only necessary for classifiers, but printing it every iteration keeps me sane)
            
            print(f'Fitting a {self.estimator.__class__.__name__} estimator, {X.shape} training set. {self.kwargs}, cutoff: {cutoff}')
            
        if self.kind=='classifier':
            self.estimator.fit(X, y<cutoff)
        elif self.kind=='regressor':
            self.estimator.fit(X, y)
        elif self.kind=='rank_regressor':
            ranks = y.argsort().argsort()+1 #most negative score becomes 1
            #logitranks = logit((ranks)/ (y.shape[0]+1)) #most negative score becomes most negative logitrank
            self.estimator.fit(X, ranks)
        else:
            raise ValueError('Got to set `kind` as either `classifier` or `regressor`, or `rank_regressor`')
        if self.verbose:
            end = time.time()
            print('Time:', end - start)

    def predict(self, X):
        """Got to return `predict` for regressors, and `predict_proba` for classifiers"""
        if self.kind=='classifier':
            try:
                preds = self.estimator.predict_proba(X)[:,1] #return the positive class probabilities=
            except:
                preds = self.estimator.decision_function(X) #like proba, higher is better!
            return preds
        elif self.kind in ['regressor', 'rank_regressor']:
            preds = -1 * self.estimator.predict(X) # we want the most negative scores to be the most positive predictions
            return preds
        else:
            raise ValueError('Got to set `kind` as either `classifier` or `regressor`')

    def chunked_predict(self, X, num_chunks=200):
        """Chunked predict just predicts for all ligands in 20 chunks. This is because
        for higher fingerprint sizes, the whole array won't fit in memory when predicting."""
        if self.verbose:
            print('\tpredicting:')
            start = time.time()
        preds = list()
        for chunk in np.array_split(np.arange(X.shape[0]),50):
            preds.append(self.predict(X[chunk]))
        if self.verbose:
            end = time.time()
            print('Time:', end - start)
        return np.concatenate(preds)
            
    def get_estimator(self):
        return self.estimator
