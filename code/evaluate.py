import numpy as np

from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

from tqdm import tqdm
import bitstring


def Evaluator():
    """Some docs: """
    def __init__(fingerprint, fpsize, smifile):
        self.fingerprint=fingerprint
        self.fpsize=fpsize
        self.fingerprint_function = getFingerprintFunction()
        self.smifile = smifile+'_short.smi'
        self.scores = np.load(self.smifile+'_short.npy')
        
    def get_fingerprint_function():
        if self.fingerprint=='morgan':
            gen_mo = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=self.fpsize)
        return gen_mo.GetFingerprint

    
    def write_fingerprints():
        """Writes one of the rdkit fingerprints to a binary file (to save storage space)
        Probably a more modern option is HDF5 but this works for now."""

        binfile = open('../processed_data/fingerprints.bin', 'wb') #writing to this file.
        smifile = open(self.smifile)
        smifile.readline() #read past the header.

        num_lines = sum(1 for line in open(self.smifile))

        #iterate through file, 
        for line in tqdm(smifile, total=num_lines, smoothing=0):
            words = line.split(',')
            scores.append(float(words[1]))
            mol = Chem.MolFromSmiles(words[0])
            fp = self.fingerprint_function(mol)
            bs = bitstring.BitArray(bin=fp.ToBitString())
            binfile.write(bs.bytes)

        binfile.close()
        smifile.close()

