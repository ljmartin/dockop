

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

python main.py morgan 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py maccs 168 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py atompair 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py topologicaltorsion 128 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
python main.py pattern 128  ../processed_data/evaluation_estimators.json ../processed_data/AmpC
