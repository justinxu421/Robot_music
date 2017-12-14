# This file produces the input file(.csv) for our algorithm given the urls of the
# beatmakers scraped from twitter and online. The CLI, along with twitterscraper,
# was used to scrape urls of beatmaker from twitter into tweets.json file
# Command: twitterscraper %23beatmaker%20splice -o tweets.json

# Import libraries
import requests
import csv
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools
import time
import json

#gets the urls scraped from twitter stored in twitter.json
listUrl = []
inputFile = open('tweets.json')
data = json.load(inputFile)
for i in range(0, len(data)):
    text = data[i]["text"]
    if text.find("https://splice.com/sounds/beatmaker/") != -1:
        listUrl.append(text[text.find("beatmaker/") + 10: text.find("\u00a0\u2026")])
inputFile.close()

#writes to the file an array of instruments and whether the beats are on
#for each song
with open("new_songs_data(incl.twitter).csv", 'w') as archive_file:
    f = csv.writer(archive_file)

    listInstr = ["Kick Drum", "Snare", "Closed Hihat", "Open Hihat", "Tom", \
    "Percussion", "FX", "Synth Hit"]
    urlList = ["fcd55ad47bbe", "d5505332a023", "krne", "kshmr", "dot-dat-genius"\
    , "lex-luger", "pbn", "mdl", "capsun", "jordy-dazz", "hellberg",\
    "0a02e924eed3", "wakaflocka", "697d2f14b599", "9c7b77a9a24f", \
    "7338392e14a3", "cf7ba3286108", "3646a4728ba2", \
    "1a2462a2c7d5?utm_source=on_site&utm_medium=cta&utm_campaign=mc_808"]
    #combines the set of urls from twitter and ones searched manually
    totalUrl = set(listUrl) | set(urlList)
    size = 32
    attribNum = len(listInstr) * size
    listAtrributes = [[instr + str(x) for x in range(0, size)] for instr in listInstr]
    f.writerow(list(itertools.chain.from_iterable(listAtrributes)))

    driver = webdriver.Chrome()

    url = 'https://splice.com/sounds/beatmaker/'

    count = 0
    for partUrl in totalUrl:
        count += 1
        print(count)
        listZeroes = [0 for x in range(0, attribNum)]
        #opens up the browser to scrape the beats from each url
        driver.get(url + partUrl)

        # waiting for the page to load
        wait = WebDriverWait(driver, 10)
        time.sleep(2)
        data = driver.page_source
        soup = BeautifulSoup(data, "html.parser")

        entries = soup.select('div[class*="sequencer-column sequencer-step"]')

        for i, entry in enumerate(entries):
            for index, elem in enumerate(entry):
                if "on-full" in str(elem.encode('utf-8')):
                    listZeroes[(index - 2) * 32  + i] = 1

                if index == 9:
                    break

        f.writerow(listZeroes)

    driver.close()
