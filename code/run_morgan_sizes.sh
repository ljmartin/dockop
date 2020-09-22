

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

python main.py morgan 64 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py morgan 128 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py morgan 256 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py morgan 512 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py morgan 1024 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py morgan 2048 ../processed_data/logreg_only.json ../processed_data/AmpC


