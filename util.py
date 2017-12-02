from collections import defaultdict
import random as rand

NUM_BEATS = 32 #number of blocks per row
NUM_INSTRUMENTS = 8 #number of rows
NUM_DATA_FEATURES = NUM_BEATS * NUM_INSTRUMENTS #total features per line

'''
    Return a tuple in the form (i,0,1,0,1), where i is the index of the block,
    and the other entries are the conditional assignments for 
    (i-1, i-n, i-2n, ...), if the index is applicable
    where n is the number of blocks per row

    The factor graph looks something like :
    o - o - o - o - o - o
    |   |   |   |   |   |
    o - o - o - o - o - o 
    |   |   |   |   |   |
    o - o - o - o - o - o
    |   |   |   |   |   |
    o - o - o - o - o - o
    with additional connections between all the rows.
'''
def createTuple(i,line):
    conditionList = [i]
    if i%NUM_BEATS != 0: #if not first entry in row
        conditionList.append(line[i-1])
    index = i
    if index > NUM_BEATS:
        index -= NUM_BEATS
        conditionList.append(line[index])
    return tuple(conditionList)

# Generate a set of on/off configurations given the probabilities of the squares
def generate(conditionalProbs):
    line = ['0']*NUM_DATA_FEATURES 
    #set all to 0 at first
    for i in range(NUM_DATA_FEATURES):
        createTuple(i,line)
        prob = conditionalProbs[createTuple(i,line)]
        line[i] = '1' if rand.random() < prob else '0'
    return list(map(int, line))

def getConditionalProbs(dataFile):
    
    probabilityCountMap = defaultdict(lambda: [0,0]) 
    '''
        map of the counts of the conditional probabiliies, keys are tuples as defined above 
        and the values are 2 sized list of the form (#0 assigned, #1 assigned)
        Initial assignment can also be changed to account for laplace smoothing
    '''

    fp = open(dataFile,'r')
    for sampleNumber,line in enumerate(fp):
        if sampleNumber == 0: 
            continue
        line = line.split(',')
        for i in range(len(line)): 
            key = createTuple(i,line)
            val = int(line[i])
            probabilityCountMap[key][val] += 1 
            #Change the counts for 0 assignment and 1 assignemnt
    fp.close()

    probabilitiesMap = defaultdict(float)
    for key,val in probabilityCountMap.items():
        probabilitiesMap[key] = float(val[1])/(val[0]+val[1])
        #calculate the probalities for each key
    return probabilitiesMap

dataFile = "new_songs_data(incl. twitter).csv"
conditionalProbs = getConditionalProbs(dataFile)
print(conditionalProbs, flush = True)

randomMusic = generate(conditionalProbs)
print(randomMusic, flush = True)
