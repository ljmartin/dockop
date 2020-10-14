import sys
from set_up import Setup
import json
import numpy as np
import tqdm
from scipy import sparse
from joblib import Parallel, delayed
from sklearn.metrics import average_precision_score


def fast_dice(X, Y=None):
    """Calculates Dice distance between a bunch of molecules,
    utilising sparse calculations for super fast results.
    Warning - results are dense matrices, beware of memory!
    If only X is given, this returns a dense pairwise distance
    matrix (like squareform(pdist(X)). If X and Y are given, 
    this returns a X.shape[0] by Y.shape[0] matrix, like
    cdist(X, Y, metric='dice')"""
    
    if X.dtype == np.bool:
        X = X.astype(int)
    if isinstance(X, np.ndarray):
        X = sparse.csr_matrix(X).astype(bool).astype(int)
    if Y is None:
        Y = X
    else:
        if isinstance(Y, np.ndarray):
            Y = sparse.csr_matrix(Y).astype(bool).astype(int)
            
    if Y.dtype == np.bool:
        Y = Y.astype(int)
            
    intersect = X.dot(Y.T)
    #cardinality = X.sum(1).A
    cardinality_X = X.getnnz(1)[:,None] #slightly faster on large matrices - 13s vs 16s for 12k x 12k
    cardinality_Y = Y.getnnz(1) #slightly faster on large matrices - 13s vs 16s for 12k x 12k
    return (1-(2*intersect) / (cardinality_X+cardinality_Y.T)).A


def do_similarity(idx,fp):
    """This is a pickleable function to be used by joblib.
    It just does the fast_dice calculation, then uses argpartition
    to calculate the 1200 nearest neighbors. Int32 to save a bit on
    memory. THen it vstacks it into a single array."""
    neighbors=list()
    split_idx = np.array_split(idx, 100)
    for sidx in tqdm.tqdm(split_idx):
        neighbs = np.argpartition(fast_dice(fp[sidx], fp[setup.train_idx]), np.arange(0, 1200), axis=1)[:,:1200].astype(np.int32)
        neighbors.append(neighbs)
    return np.vstack(neighbors)


N_JOBS=8


if __name__=="__main__":
    fpType='morgan'
    dataset = '../processed_data/AmpC'
    setup = Setup(fpType, dataset)
    setup.load_fingerprints()
    setup.load_scores()
    setup.random_split(15000)
    true = setup.scores[setup.test_idx]<-60
    
    #for fpSize in 256, 512, 1024, 2048, 4096, 8192:
    for fpSize in 16384, 32768, 65536:
        fp = setup.fold_to_size(fpSize)

        #parallelize kNN calculation
        split_fps = Parallel(n_jobs=N_JOBS)(delayed(do_similarity)(i, fp) for i in np.array_split(setup.test_idx, N_JOBS))

        #put kNN indices back together
        concat_fps = np.vstack(split_fps)

        #calculate predictions in terms of True or False
        preds = setup.scores[setup.train_idx][concat_fps]<-60

        aps = list()
        for ncols in tqdm.tqdm(range(1,1201)):
            ap = average_precision_score(true, preds[:,:ncols].mean(axis=1))
            aps.append(ap)

        np.save('../processed_data/knn_'+str(fpSize)+'.npy', aps)
