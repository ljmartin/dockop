import n2
import numpy as np
from pathlib import Path
import tqdm

class KNNClassifier(object):
    def __init__(self, fingerprint_kind, dimension, verbose):
        self.fingerprint_kind = fingerprint_kind
        self.dimension = dimension
        self.verbose=verbose

        
    def build_ann_index(self, fingerprints, nthreads=1, overWrite=False):
        """WARNING: set threads correctly! I set it to 1 so you don't run out of memory.
        This builds an approximate nearest neighbors index, used to build a kNN graph.
        n2 is a good choice because it is fast and also allows streaming upload. Further,
        it outperforms many other libraries according to ann_benchmarks. n2 is awesome.
        It does not, however, offer dice, jaccard, or tanimoto. In practice cosine works fine."""


        index_file = Path("../processed_data/"+self.fingerprint_kind+'_n2_index.hnsw')
        
        if index_file.is_file() and not overWrite:
            raise Exception('Index file exists already. Set `overWrite` to true to re-write it')
        else:
            pass


        if not isinstance(fingerprints, np.ndarray):
            if self.verbose:
                print('converting to numpy')
            fingerprints = fingerprints.toarray()

        if self.verbose:    
            print('adding vector data to n2')

        index = n2.HnswIndex(self.dimension, "angular")
        for fp in tqdm.tqdm(fingerprints,smoothing=0):
            index.add_data(fp)

        if self.verbose:
            print(f'building index with {nthreads}')
            
        index.build(n_threads=nthreads)
        index.save('../processed_data/'+self.fingerprint_kind+'_n2_index.hnsw')
        


    
