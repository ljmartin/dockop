

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC


#for trainingSize in 300 416 577 800 1110 1539 2135 2961 4107 5696 7900 10956 15196 21075 29230 40540 56226 77981 108153 150000; do
for trainingSize in 280000 400000; do
    python main.py morgan_feat 32768 $trainingSize ../processed_data/logreg_only.json ../processed_data/AmpC
done
