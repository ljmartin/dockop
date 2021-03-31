# dockop

Ultra-large scale (100 to 1000 million ligands) virtual molecule libraries are now available from suppliers like Enamine or WuXi. The increased size yields better diversity of high-scoring molecules in a docking campaign, but requires more infrastructure like high-performance computing clusters. The aim of this project was to show that the same hits coud be identified without docking the entire library. By training a surrogate model on a random sample of ligands and their docking scores. The approach uses just _sklearn_'s LogisticRegression and _RDKit_'s Morgan fingerprints with pharmacophoric atom invariants.

[1] Lyu, Jiankun, et al. "Ultra-large library docking for discovering new chemotypes." Nature 566.7743 (2019): 224-229.


### results:

![fpcomp](./processed_data/fpsize_logreg.svg)

Interestingly, simply increasing the size of fingerprints beyond what is commonly used in the field (2,048) improves performance a lot! In addition, Morgan fingerprints, often considered a starting point, perform best. Actually, when you use larger Morgan fingerprints they can perform at least as well as a graph neural network:

![active](./processed_data/active_learning_percentage.svg)

The manuscript just uses LogisticRegression with default settings because I found that performs	best consistently. But you might be interested in trying other classifiers, hyperparameters
, or regressors. If so,	check out this bonus figure first. It might look like Ridge regressors perform best, and they do perform well, but I found it didn't carry through to the iterative docking retrieval task.

![algo_fp_comparison](./processed_data/fpsize_figure.svg)

### discussion

The ROC curve from a simple test/train split using LogisticRegression is almost perfect. Why does such a simple technique perform so well at predicting docking scores? Compare to bioactivity virtual screening - LogReg and Morgan fingerprints are actually criticized a lot for not generalizing. Perhaps the shift to true random sampling of the training and test sets (as opposed to highly biased sampling in bioactivity data) complies better with the assumptions behind logistic regression, and increases the actual chemical diversity beyond what you would have for the same number of ligands in, say, ChEMBL.     

### reproduce any of the figures

Use this environment:

`conda env create -f dockop.yml`

and look in `./code` for instructions.
