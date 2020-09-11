

# commands:

select N ligands from the 99million in the AmpC screen:

```
conda activate dockop

python parse_data.py ../data/AmpC_screen_table.csv 2000000 ../processed_data/AmpC_short.csv


```
