import sys
from set_up import Setup
from estimator import CommonEstimator
import json
import h5py
from utils import get_memory_usage

import numpy as np
SEED = 12939 #from random.org
np.random.seed(SEED)



print('python main.py fpType fpSize estimators.json dataset')

fpType = sys.argv[1]
fpSize = int(sys.argv[2])
trainingSetSize = int(sys.argv[3])
json_name = sys.argv[4]
dataset = sys.argv[5]


print('Running:')
print(f'python main.py {fpType} {fpSize} {json_name} {dataset}')


estimators = json.load(open(json_name, 'r'))['estimators']

if __name__=='__main__':
    #setup the data:
    setup = Setup(fpType, dataset, verbose=True)
    try:
        setup.write_fingerprints()
    except:
        print('Already written fpfile')        
    setup.load_fingerprints()
    setup.load_scores()
    
    feature_matrix = setup.fold_to_size(fpSize)
    
    #evaluation stuff goes here:    
    for estimator in estimators:
        for repeat in range(5):
            setup.random_split(trainingSetSize)
                
            common_estimator = CommonEstimator(estimator, cutoff=0.8, verbose=setup.verbose)
            print(setup.train_idx.shape)
            print(setup.scores.shape)
            common_estimator.fit(feature_matrix[setup.train_idx], setup.scores[setup.train_idx])
            pred = common_estimator.chunked_predict(feature_matrix[setup.test_idx])

            setup.write_results(pred, fpSize, trainingSetSize, estimator['name'], repeat)
                
