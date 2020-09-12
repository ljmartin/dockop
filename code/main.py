import sys
from set_up import Setup
from evaluate import Evaluator

from utils import get_memory_usage

if sys.argv[1]==None or sys.argv[2]==None or sys.argv[3]==None:
    print('Follow instructions at https://github.com/ljmartin/dockop/tree/master/code: python main.py fpType fpSize dataset')

fpType = sys.argv[1]
fpSize = sys.argv[2]
dataset = sys.argv[3]

if __name__=='__main__':
    setup = Setup(fpType, fpSize, dataset)
    setup.write_fingerprints()
    setup.load_fingerprints()

    #paris clustering. The alternative would be MiniBatchKMeans (below),
    #which to be honest is much faster and easier. However it's based on
    #assumptions that don't apply to ligand vector data, like normally
    #distributed clusters and no noise - these are clearly not true!
    setup.build_ann_index(nthreads=8)
    setup.build_knn_graph(15)
    setup.fit_paris()
    setup.cluster('balanced', 25)
    
    #from sklearn.cluster import MiniBatchKMeans
    #clst = MiniBatchKMeans(n_clusters=10000, batch_size=10000)
    #clst.fit(setup.fingerprints)
    #setup.clusters=clst.labels_

    for training_size in [1000, 3000, 10000, 30000, 100000]:
        for _ in range(3):
            setup.random_split()

            #evaluation stuff goes here:
