
import numpy as np
import random as rand

numDataFeatures = 9 # Change 9 to 16 * 8 with full file
numDataPoints = -1
dataSum = [0] * numDataFeatures

dataFile = "fakeData.txt"
fp = open(dataFile,'r')
for _,line in enumerate(fp):
    numDataPoints += 1
    if numDataPoints == 0: continue
    for i in range(len(line)): 
        if line[i].isdigit():
            dataSum[i / 3] += int(line[i]) # Change 3 to whatever you need to 
fp.close()

print numDataPoints
print dataSum

dataProbs = [x / (1.0 * numDataPoints) for x in dataSum]
print dataProbs

def generate(dataProbs):
    result = [ 1 if rand.random() < prob else 0 for prob in dataProbs ]
    return result

for _ in range(10):
    print generate(dataProbs)



