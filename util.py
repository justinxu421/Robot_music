from collections import defaultdict
import random as rand
import numpy as np
import sys

'''
    utility file that has all the functions necessary for generation
'''

NUM_BEATS = 32 #number of blocks per row
NUM_INSTRUMENTS = 8 #number of rows
NUM_DATA_FEATURES = NUM_BEATS * NUM_INSTRUMENTS #total features per line

''' 
    Outdated MLE algorithm
'''
def getMLEProbs(dataFile):
    numDataFeatures = 8 * 32 
    numDataPoints = -1
    dataSum = [0] * numDataFeatures

    fp = open(dataFile,'r')
    for _,line in enumerate(fp):
        numDataPoints += 1
        if numDataPoints == 0: continue
        for i in range(len(line)): 
            if line[i].isdigit():
                dataSum[i // 2] += int(line[i]) # Change to adjust to data
    fp.close()

    dataProbs = [x / (1.0 * numDataPoints) for x in dataSum]
    return dataProbs

'''
    Return a tuple in the form (i,0,1,0,1), where i is the index of the block,
    and the other entries are the conditional assignments for 
    (i-1, i-n), if the index is applicable
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
    if index >= NUM_BEATS:
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

#Get the conditional probabilities from the files given
def getConditionalProbs(files):
    probabilityCountMap = defaultdict(lambda: [0,0]) 
    '''
        map of the counts of the conditional probabiliies, keys are tuples as defined above 
        and the values are 2 sized list of the form (#0 assigned, #1 assigned)
        Initial assignment can also be changed to account for laplace smoothing
    '''
    for file,line in files.items():
        for i in range(len(line)): 
            key = createTuple(i,line)
            val = int(line[i])
            probabilityCountMap[key][val] += 1 
            #Change the counts for 0 assignment and 1 assignemnt

    probabilitiesMap = defaultdict(float)
    for key,val in probabilityCountMap.items():
        probabilitiesMap[key] = float(val[1])/(val[0]+val[1])
        #calculate the probalities for each key
    return probabilitiesMap

#converts the datafile into a dictionary with form {file number: assignment}
def datafileToDict(datafile):
    fp = open(datafile,'r')
    files = dict()
    for i,line in enumerate(fp):
        if i == 0:
            continue
        files[i-1] = line.split(',') #make an array
    return files

#get the Counts for the songs for running k-means on
def getSongNoteCount(files):
    fileCounts = defaultdict(int)
    for file,line in files.items():
        count = sum(list(map(int,line)))
        fileCounts[file] = count
    return fileCounts

#run k-means to cluster the files by densities
def kMeans(fileCounts,k):
    numFiles = len(fileCounts)
    centroids = [0]*k
    #centroids hold the count densities
    assignments = [0]*numFiles
    #holds the centroid assignment for each file
    for i in range(k):
        randFile = rand.randint(1,numFiles)
        centroids[i] = fileCounts[randFile]
        #assign the centroids to a random count
    oldCentroids = [0]*k
    count = 0
    while np.linalg.norm(np.array(centroids) - np.array(oldCentroids)) > 1e-3:
        oldCentroids = centroids[:]
        count += 1
        for i in range(numFiles):
            minNum = -1
            for cluster in range(k):
                distance = abs(centroids[cluster] - fileCounts[i])
                if cluster == 0:
                    minNum = distance
                    assignments[i] = cluster
                elif distance < minNum:
                    minNum = distance
                    assignments[i] = cluster
                #update cluster

        clusterSumAndCounts = defaultdict(lambda: [0,0])
        #dictionary that is of form {cluster: [sum of densities, number assigned to cluster]}
        for i in range(numFiles):
            cluster = assignments[i]
            clusterSumAndCounts[cluster][0] += fileCounts[i] #sums up densities
            clusterSumAndCounts[cluster][1] += 1 #sums up number asisgned to cluster
        for centroid in range(k):
            if(clusterSumAndCounts[centroid][1] == 0):
                centroids[centroid] = sys.maxsize #if none assigned, set to infty
            else:
                centroids[centroid] = float(clusterSumAndCounts[centroid][0]) / clusterSumAndCounts[centroid][1]
                #update centroid
    #print("count is", count)
    return assignments, centroids

#function that probabilistically creates an assignment
def makeAssignment():
    dataFile = "new_songs_data(incl. twitter).csv"
    files = datafileToDict(dataFile) #convert to map
    fileCounts = getSongNoteCount(files) #get map of counts
    assignments,centroids = kMeans(fileCounts,3) #run k means to find assignments

    print("centroid values:", centroids)
    maxIndex = centroids.index(max(centroids)) 
    minIndex = centroids.index(min(centroids))
    middleIndex = 3 - maxIndex - minIndex #works since sum of all 3 is 0+1+2 = 3

    filesInCluster = dict() #files in appropriate cluster
    for i in range(len(assignments)):
        if assignments[i] == minIndex: #this parameter can be adjusted
            filesInCluster[i] = files[i]
    print("number of files in cluster:", len(filesInCluster))

    conditionalProbs = getConditionalProbs(filesInCluster)
    #get the probability table

    randomMusic = generate(conditionalProbs)
    #create a random music assignment
    print("assignment is", randomMusic)
    return randomMusic

# Cut makeAssignment() off and return the conditional probabilities
def getConditionalProbsFromScratch(cluster):
    dataFile = "new_songs_data(incl. twitter).csv"
    files = datafileToDict(dataFile) #convert to map
    fileCounts = getSongNoteCount(files) #get map of counts
    assignments,centroids = kMeans(fileCounts,3) #run k means to find assignments

    #print("centroid values:", centroids)
    maxIndex = centroids.index(max(centroids)) 
    minIndex = centroids.index(min(centroids))
    middleIndex = 3 - maxIndex - minIndex #works since sum of all 3 is 0+1+2 = 3

    desiredIndex = 0
    if cluster == "min":
        desiredIndex = minIndex 
    elif cluster == "max":
        desiredIndex = maxIndex
    elif cluster == "middle": 
        desiredIndex = middleIndex
    else: 
        desiredIndex = -1 #take all of them! 

    filesInCluster = dict() #files in appropriate cluster
    for i in range(len(assignments)):
        if assignments[i] == desiredIndex or desiredIndex == -1: 
            filesInCluster[i] = files[i]
    print("number of files in cluster:", len(filesInCluster))

    return getConditionalProbs(filesInCluster)

makeAssignment()
