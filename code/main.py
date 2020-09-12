import sys
from set_up import Setup
from estimator import CommonEstimator

import json
import h5py

from utils import get_memory_usage

print('python main.py fpType fpSize estimators.json dataset')
print('for example:')
print('python main.py morgan 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC')

fpType = sys.argv[1]
fpSize = int(sys.argv[2])
json_name = sys.argv[3]
dataset = sys.argv[4]

estimators = json.load(open(json_name, 'r'))['estimators']

if __name__=='__main__':
    setup = Setup(fpType, fpSize, dataset, verbose=True)
    setup.write_fingerprints()
    setup.load_fingerprints()
    setup.load_scores()
    
    ##paris clustering. The alternative would be MiniBatchKMeans (below),
    ##which to be honest is much faster and easier. However it's based on
    ##assumptions that don't apply to ligand vector data, like normally
    ##distributed clusters and no noise - these are clearly not true!
    #setup.build_ann_index(nthreads=8)
    #setup.build_knn_graph(15)
    #setup.fit_paris()
    #setup.cluster('balanced', 25)
    
    #from sklearn.cluster import MiniBatchKMeans
    #clst = MiniBatchKMeans(n_clusters=10000, batch_size=10000)
    #clst.fit(setup.fingerprints)
    #setup.clusters=clst.labels_

    for training_size in [10000]:
        #evaluation stuff goes here:
        for estimator in estimators:

            for repeat in range(3):
                setup.random_split(training_size)
                
                common_estimator = CommonEstimator(estimator, setup.verbose)
                common_estimator.fit(setup.fingerprints[setup.train_idx], setup.scores[setup.train_idx])
                pred = common_estimator.predict(setup.fingerprints[setup.test_idx])

                setup.write_results(pred, estimator['name'], repeat)
                
