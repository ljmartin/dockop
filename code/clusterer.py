import n2
from sknetwork.hierarchy import Paris
from sknetwork.hierarchy import cut_balanced, cut_straight


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


from sknetwork.hierarchy import Paris
from sknetwork.hierarchy import cut_balanced, cut_straight


    def build_ann_index(self, nthreads=1):
        """WARNING: set threads correctly! I set it to 1 so you don't run out of memory.
        This builds an approximate nearest neighbors index, used to build a kNN graph.
        n2 is a good choice because it is fast and also allows streaming upload. Further,
        it outperforms many other libraries according to ann_benchmarks. n2 is awesome.
        It does not, however, offer dice, jaccard, or tanimoto. In practice cosine works fine."""

        if self.verbose:
            print('adding vector data to n2')
        index = n2.HnswIndex(self.fpsize, "angular")
        for fp in self.fingerprints:
            index.add_data(fp)

        if self.verbose:
            print(f'building index with {nthreads}')
            
        index.build(n_threads=nthreads)
        index.save('../processed_data/n2_index.hnsw')



    def build_knn_graph(self, k):
        """Builds a kNN graph using the approx. NN index built earlier. In practice,
        in most nearest neighbor settings going above k=25 doesn't reall add any benefit."""

        if self.verbose:
            print(f'constructing kNN graph with k={k}')
            
        index = n2.HnswIndex(self.fpsize, "angular")
        index.load('../processed_data/n2_index.hnsw')

        data = list()
        indices = list()
        indptr = list()
        count = 0
        indptr.append(count)
        
        for i in tqdm(range(self.num_ligs)):
            neighbor_idx = index.search_by_id(i,k,100, include_distances=True)[1:]
            for nidx, distance in neighbor_idx:
                data.append(1-distance)
                indices.append(nidx)
                count+=1
            indptr.append(count)

        self.adj = sparse.csr_matrix( ( data, indices, indptr), shape=(self.num_ligs, self.num_ligs), dtype=np.float16)

        #do a check that the values in the adjacency matrix are in the right place:
        for _ in range(50):
            idx = np.random.choice(self.num_ligs)
            adjacency_indices = self.adj[idx].indices
            adjacency_distances = 1-self.adj[idx].data
            query = index.search_by_id(idx, k, 100, include_distances=True)[1:]
            index_indices = [i[0] for i in query]
            index_distances = [i[1] for i in query]
            assert np.allclose(index_distances, adjacency_distances, atol=1e-3) #high tolerance because np.float16 conversion.
            assert np.allclose(adjacency_indices, index_indices)

    def fit_paris(self):
        """ Uses a super useful library scikit-network to fit a PARIS clusterer on the kNN graph.
        PARIS clustering is hierarchical, so it returns a dendrogram instead of clusters. Later we cut the dendrogram.
        see: Hierarchical Graph Clustering using Node Pair Sampling by Bonald et al  https://arxiv.org/abs/1806.01664"""

        if self.verbose:
            print('fitting PARIS hierarchical clustering')
        paris = Paris()        
        paris.fit(self.adj)
        self.dendrogram = paris.dendrogram_

    def cluster(self, method, n_clust=None, threshold=None):
        """Cuts the dendrogram and returns cluster IDs. Straight cuts can either
        set a defined number of clusters, or alternatively set a distance threshold. 
        Cluster sizes can vary widely.
        
        Balanced cuts respect a maximum cluster size. The number of clusters is determined 
        on the fly. """

        if self.verbose:
            print(f'clustering with a {method} cut')
        
        if method == 'straight':
            if n_clust is not None and threshold is not None:
                raise ValueError('Straight cut takes only one of n_clusters or threshold, not both.')
            self.clusters = cut_straight(self.dendrogram, n_clust, threshold)
        elif method == 'balanced':
            if n_clust is None:
                raise ValueError('Must set maximum cluster size (n_clust) for balanced_cut')
            self.clusters = cut_balanced(self.dendrogram, n_clust)
        else:
            print('Choose \"straight\" or \"balanced\"')
