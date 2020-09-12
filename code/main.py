import sys
from set_up import Setup
from estimator import CommonEstimator

import json
import h5py

from utils import get_memory_usage

if sys.argv[1]==None or sys.argv[2]==None or sys.argv[3]==None:
    print('Follow instructions at https://github.com/ljmartin/dockop/tree/master/code: python main.py fpType fpSize estimators dataset')

fpType = sys.argv[1]
fpSize = sys.argv[2]
json_name = sys.argv[3]
dataset = sys.argv[4]

estimators = json.load(open(json_name, 'r'))['estimators']

if __name__=='__main__':
    setup = Setup(fpType, fpSize, dataset, verbose=True)
    setup.write_fingerprints()
    setup.load_fingerprints()

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

    for training_size in [20000]:
        #evaluation stuff goes here:
        for estimator in estimators:
            outf = h5py.File('../processed_data/fpType_'+estimator['name']+'.hdf5', 'w')

            for repeat in range(3):
                common_estimator = CommonEstimator(estimator)
                common_estimator.fit(setup.fingerprints[setup.train_idx], setup.scores[setup.train_idx])
                pred = common_estimator.predict(setup.fingerprints[setup.test_idx])

                #write the test indices and predicted scores to the HDF5:
                rp = outf.create_group(f'repeat{repeat}')
                dset_idx = rp.create_dataset('test_idx', setup.test_idx.shape, dtype='int')
                dset_idx[:] = setup.test_idx

                dset_pred = grp1.create_dataset('prediction', pred.shape, dtype='float16')
                dset_pred = pred
            outf.close()
