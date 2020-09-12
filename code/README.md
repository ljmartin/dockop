

# commands:

select N ligands from the 99million in the AmpC screen:

```
conda activate dockop

python parse_data.py ../data/AmpC_screen_table.csv 2000000 ../processed_data/AmpC_short.csv

```

then choose a fingerprint (from 'morgan', 'atompair', 'rdk', ...tba) and a fingerprint size.

The following will generate the fingerprint file in binary, of a given size (128 below)
then fetch a bunch of sklearn estimators from `../processed_data/evaluation_estimators.json`
and evaluate them.

```
python main.py morgan 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC

```