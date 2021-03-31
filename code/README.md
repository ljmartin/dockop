

# fingerprint comparison

It takes about 8-10 hours to fingerprint 100 million ligands, and I did a lot of testing of different estimators in sklearn. To speed up the algorithm/fingerprint comparison, it's performed on a subset of the AmpC data. select N ligands from the 99million in the AmpC screen. The bash script `run_all.sh` will parse the AmpC dataset, selecting ~1,000,000 ligands at random to fingerprint in each of `morgan`, `atompair`, `rdk`, `pattern`, `topologicaltorsion`. I also tried `maccs` but it really didn't compare well. 

```
conda activate dockop

bash run_all.sh
```

# full AmpC and D4 datasets, single and multiple iterative docking

These use notebooks. Run `AmpC_` or `D4_` `*all_generate_FPs.ipynb` to generate sparse Morgan fingerprints with pharmacophoric features for the whole datasets, since they performed best in the fingerprint comparison. You'll note that 100 million fingerprints won't fit in memory unless you have a nice computer, so I chunked it into 10,000,000-sized blocks. I suggest this is a great way to perform iterative docking on your own workstation!

Single iteration docking can be performed in `AmpC_` or `D4_` `*_all_single.ipynb`. 
