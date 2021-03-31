

python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

for fp in morgan pattern rdk topologicaltorsion morgan_feat atompair; do
    for size in 128 256 512 1024 2048 4096 8192 16384 32768 65536; do
	python main.py $fp $size 50000 ../processed_data/evaluation_estimators_clf.json ../processed_data/AmpC
    done
done
