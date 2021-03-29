

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC
#for trainingSize in 300 416 577 800 1110 1539 2135 2961 4107 5696 7900 10956 15196 21075 29230 40540 56226 77981 108153 150000 280000 400000; do
for trainingSize in 1000 1611 2598 4188 6752 10884 17546 28284 45594 73497 118477 190985 307866 496279 800000; do
    python main.py morgan_feat 8192 $trainingSize ../processed_data/logreg_only.json ../processed_data/AmpC
done
