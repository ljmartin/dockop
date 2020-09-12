from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, SGDClassifier, ElasticNet, Lasso
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC, SVR
from sklearn.gaussian_process import GaussianProcessClassifier

DOCKING_SCORE_CUTOFF = -60

class CommonEstimator(object):
    """ This class just provides a common interface for both classifiers and regressors.
    Makes things easier in the evaluation stage, I can just iterate through estimator:parameter 
    pairs from a JSON and it will work."""
    def __init__(self, parameters, verbose=False):
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
        self.cutoff = DOCKING_SCORE_CUTOFF
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
            print(f'Fitting a {self.estimator.__class__.__name__} estimator')
            
        if self.kind=='classifier':
            self.estimator.fit(X, y<self.cutoff)
        elif self.kind=='regressor':
            self.estimator.fit(X, y)
        else:
            raise ValueError('Got to set `kind` as either `classifier` or `regressor`')

    def predict(self, X):
        """Got to return `predict` for regressors, and `predict_proba` for classifiers"""
        if self.kind=='classifier':
            try:
                return self.estimator.predict_proba(X)[:,1] #return the positive class probabilities
            except:
                return self.estimator.decision_function(X) #like proba, higher is better!
        elif self.kind=='regressor':
            return -1 * self.estimator.predict(X) # we want the most negative scores to be the most positive predictions
        else:
            raise ValueError('Got to set `kind` as either `classifier` or `regressor`')

    def get_estimator(self):
        return self.estimator
