

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

for size in 83 166; do
    python main.py maccs $size 15000 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
done
