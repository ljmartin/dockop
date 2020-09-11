import sys
import json
from evaluate import Evaluator


fingerprint = sys.argv[1]
fpsize = sys.argv[2]
algorithms = json.loads(sys.argv[3])

if __name__=="__main__":
    evaluator = Evaluator(fingerprint, fpsize)

    #write out a binary file with the fingerprints:
    evaluator.write_fingerprints()

    
    
