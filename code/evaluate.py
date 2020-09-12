import numpy as np
from scipy import sparse

from 


DOCKING_SCORE_CUTOFF = -60


#NOT the sklearn base estimator. 
class BaseEst(object):
    def __init__(self):
        self.cutoff = DOCKING_SCORE_CUTOFF
        self.estimator = None

    def fit(self):
        pass

    def predict(self):
        pass

    def getEstimator(self):
        return self.estimator

class lr(BaseEst):
    

class Evaluator(object):
    def __init__(self):
        pass

    
        
