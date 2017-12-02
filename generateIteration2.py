import numpy as np
import random as rand
import time 
import util

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

'''
    File which handles all the overhead of automatically clicking the elements in the browser
'''

# Get the probability of each square from the data file 
'''def getDataProbs(dataFile):
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
    return dataProbs'''

# Start up the page, close the annoying things, then turn all existing notes off 
def startPage():
    driver = webdriver.Firefox()
    driver.get("https://splice.com/sounds/beatmaker")

    for _ in range(4):
        button = driver.find_element(By.XPATH, "//i[@class='fa fa-close']")
        button.click()
    
    button = driver.find_element(By.XPATH, "//i[@class='fa fa-times-circle']")
    button.click()

    return driver

# Convert from the data file indexing to the xpath indexing 
def dataToXpath(index):
    col = index % 32
    row = index // 32 
    return 8 * col + row + 1

# Click the specififed button (xpath indexed)
def clickInstrumentButton(driver, index):
    request = "(//div[@class='active-overlay'])[" + str(index) + "]"
    print(request, flush = True)
    button = driver.find_element(By.XPATH, request)
    button.click()

# Turn the buttons that were specified in the configuration on
def inputToPage(driver, randomMusic):
    for i in range(0, len(randomMusic)):
        if randomMusic[i] == 1:
            xpathIndex = dataToXpath(i) 
            clickInstrumentButton(driver, xpathIndex)

#get the assignments
randomMusic = util.makeAssignment()

driver = startPage()
inputToPage(driver, randomMusic)