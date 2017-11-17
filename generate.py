
import numpy as np
import random as rand
import time 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def getDataProbs(dataFile):
    numDataFeatures = 9 # Change 9 to 16 * 8 with full file
    numDataPoints = -1
    dataSum = [0] * numDataFeatures

    fp = open(dataFile,'r')
    for _,line in enumerate(fp):
        numDataPoints += 1
        if numDataPoints == 0: continue
        for i in range(len(line)): 
            if line[i].isdigit():
                dataSum[i // 3] += int(line[i]) # Change 3 to whatever you need to 
    fp.close()

    dataProbs = [x / (1.0 * numDataPoints) for x in dataSum]
    return dataProbs

def generate(dataProbs):
    result = [ 1 if rand.random() < prob else 0 for prob in dataProbs ]
    return result

def startPage():
    driver = webdriver.Firefox()
    driver.get("https://splice.com/sounds/beatmaker")

    for _ in range(4):
        button = driver.find_element(By.XPATH, "//i[@class='fa fa-close']")
        button.click()
    
    turnedOn = [1, 6, 8, 19, 28, 32, 35, 44, 49, 61, 66, 97, 129, 147, 156, 163, 172, 177, 189, 194]
    for i in turnedOn:
        clickInstrumentButton(driver, i)

    return driver

def dataToXpath(index):
    col = index % 32
    row = index // 32 
    return 8 * col + row + 1

def clickInstrumentButton(driver, index):
    request = "(//div[@class='active-overlay'])[" + str(index) + "]"
    print(request, flush = True)
    button = driver.find_element(By.XPATH, request)
    button.click()

def inputToPage(driver, randomMusic):
    for i in range(0, len(randomMusic)):
        if randomMusic[i] == 1:
            xpathIndex = dataToXpath(i) 
            clickInstrumentButton(driver, xpathIndex)


dataFile = "fakeData.txt"
dataProbs = getDataProbs(dataFile)
print(dataProbs, flush = True)

randomMusic = generate(dataProbs)
print(randomMusic, flush = True)
driver = startPage()

inputToPage(driver, randomMusic)