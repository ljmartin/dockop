import numpy as np
import sys
from tqdm import tqdm
import random 


random.seed(733101) #from www.random.org

filename = sys.argv[1]
desired_num_ligands = sys.argv[2]
outfilename = sys.argv[3]


#find out how many ligands there are that have an associated docking score:
print('Counting ligands with docking score...')
smifile = open(filename, 'r')
smifile.readline() #read past the header.

count = 0
for line in smifile:
    words = line.split(',') 
    if words[1]=='no_score':
        break
    count+=1
smifile.close()

print(f'There were {count} ligands')
print('Randomly selecting and writing {desired_num_ligands}...')

p = int(desired_num_ligands)/count


smifile = open(filename, 'r')
smifile.readline() #read past the header.

outsmi = open(outfilename+'_short.smi', 'w')
outsmi.write('smiles\n')

scores = list()

for line in tqdm(smifile, total=count, smoothing=0):
    if random.choices([True,False], weights=[p, 1-p])[0]:
        words = line[17:-1].split(',') #removes the zinc ID and trailing newline
        if words[1]=='no_score':
            break
        else:
            scores.append(float(words[1]))
            outsmi.write(words[0]+'\n')

np.save('../processed_data/'+outfilename+'_short.npy', np.array(scores, dtype=np.float16))
outsmi.close()
smifile.close()
