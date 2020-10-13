

# commands:

select N ligands from the 99million in the AmpC screen:

```
conda activate dockop

python parse_data.py ../data/AmpC_screen_table.csv 10000000 ../processed_data/AmpC
```

then choose a fingerprint (from 'morgan', 'atompair', 'rdk', 'maccs', 'pattern', 'topologicaltorsion') and a fingerprint size.

The following will generate the fingerprint file in unfolded form (actually folded down to 65536),
then will fold it down to a normal size (128 below). Then fetch a bunch of sklearn estimators
from `../processed_data/evaluation_estimators.json` and evaluates them using random splits and
Monte Carlo Cross Validation.

```
python main.py morgan 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC

```

To perform the kNN analysis, just run `run_knn.py`. There are no options but see inside the script for what's going on or email for help. 