

python parse_data.py ../data/AmpC_screen_table.csv 2000000 ../processed_data/AmpC

python main.py maccs 168 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py morgan 256 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py atompair 256 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py topologicaltorsion 256 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py pattern 256  ../processed_data/evaluation_estimators.json ../processed_data/AmpC
