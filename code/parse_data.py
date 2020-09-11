import sys
from tqdm import tqdm
import random 



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

outsmi = open(outfilename, 'w')
outsmi.write('smiles,dockscore\n')

for line in tqdm(smifile, total=count, smoothing=0):
    if random.choices([True,False], weights=[p, 1-p])[0]:
        short = line[17:] #removes the zinc ID
        if short.split(',')[1]=='no_score':
            break
        else:
            outsmi.write(short)
outsmi.close()
smifile.close()
