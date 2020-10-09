

#python parse_data.py ../data/AmpC_screen_table.csv 1000000 ../processed_data/AmpC

python main.py topologicaltorsion 64 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 128 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 256 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 512 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 1024 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 2048 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 4096 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 8192 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 16384 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 32768 15000 ../processed_data/logreg_only.json ../processed_data/AmpC
python main.py topologicaltorsion 65536 15000 ../processed_data/logreg_only.json ../processed_data/AmpC

python main.py topologicaltorsion 64 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 128 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 256 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 512 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 1024 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 2048 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 4096 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 8192 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 16384 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 32768 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC
python main.py topologicaltorsion 65536 15000 ../processed_data/bernoulli_only.json ../processed_data/AmpC



