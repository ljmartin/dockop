

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

for size in 128 256 512 1024 2048 4096 8192 16384 32768 65536; do
    python main.py atompair $size 100000 ../processed_data/evaluation_estimators.json ../processed_data/AmpC
done
