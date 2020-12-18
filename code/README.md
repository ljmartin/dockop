

# commands:

select N ligands from the 99million in the AmpC screen:

```
conda activate dockop

python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC
```

then choose a fingerprint (from 'morgan', 'atompair', 'rdk', 'maccs', 'pattern', 'topologicaltorsion') and a fingerprint size.

The following will generate the fingerprint file in unfolded form (actually folded down to 65536),
then will fold it down to a normal size (128 below). Then fetch a bunch of sklearn estimators
from `../processed_data/evaluation_estimators.json` and evaluates them using random splits and
Monte Carlo Cross Validation.

```
python main.py morgan 128 15000 ../processed_data/evaluation_estimators.json ../processed_data/AmpC

```

To perform the kNN analysis, just run `run_knn.py`. There are no options but see inside the script for what's going on or email for help.


# Dopamine receptor type D4

Having analyzed various fingerprints, folding sizes, algorithms, and training set sizes we
are ready to simuilate a real docking campaign using the D4 receptor. Start by sampling ~40,000 ligands
from the virtual screening library:

```
python parse_data.py ../data/table_name_smi_energy_hac_lte_25_title.csv 40000 ../processed_data/D4_sample_short
```

these ligands can then be docked. Based on the evaluation of the random sample in `D4_subsample_analysis.ipynb`, we decide to sample 10,000,000 more ligands
from the virtual screening library (this is about the limit for reasonable hard disk space on a single workstation):
```
python parse_data.py ../data/table_name_smi_energy_hac_lte_25_title.csv 10000000 ../processed_data/D4_largesample
```

Then, we fingerprint the smiles codes for those ligands, rank them, and dock in order. 