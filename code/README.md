
# figure 1 - empirical hit rate

fit a GAM to the _in vitro_ hit rate data from Lyu et al. using pyGAM in `empirical_hit_rate_fit.ipynb`. 

# figure 2 - fingerprint comparison

It takes about 8-10 hours to fingerprint 100 million ligands, and I did a lot of testing of different estimators in sklearn and fingerprints in rdkit. To speed up the algorithm/fingerprint comparison, it's performed on a subset of the AmpC data. The bash script `run_all.sh` will parse the AmpC dataset, selecting ~1,000,000 ligands at random (once) to fingerprint in each of `morgan`, `atompair`, `rdk`, `pattern`, `topologicaltorsion`. I also tried `maccs` but it really didn't compare well. 

```
conda activate dockop

bash run_all.sh
```

This will save some `hdf5` files in `../processed_data`. You can generate `figure 2` in `./plot_scripts/plot_fpcomparison_figure.py`

# figures 3,4,5,6,7 - full AmpC and D4 datasets, single and multiple iterative docking

These use notebooks. Run `AmpC_` or `D4_` `*all_generate_FPs.ipynb` to generate sparse Morgan fingerprints with pharmacophoric features for the whole datasets, since these performed best in the fingerprint comparison. You'll note that 100 million fingerprints won't fit in memory unless you have a nice computer, so I chunked it into 10,000,000-sized blocks. I suggest this is a great way to perform iterative docking on your own workstation! There's a bit of extra overheading in selecting train/test sets from chunked fingerprints stored on disk, but particular when you scale up to a billion ligands, it becomes a necessity..

Data for `figure 3` showing the effect of increasing training set size can be generated in `AmpC_all_single_AveragePrecision.ipynb`. Generate `figure 3` with `./plot_scripts/plot_ampc_ap.py`

Data for single iteration docking can be generated in `AmpC_` or `D4_` `*_all_single.ipynb`.

Data for multiple iteration docking can be generated in `AmpC_` or `D4_` `*all_iterative.ipynb`. Generate `figure 4,5,6,7` with `./plot_scripts/plot_wholedataset.py`

