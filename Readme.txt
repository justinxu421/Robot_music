To get a sample of our beats, you can simply run generate.py (Python 3). You will also need to install selenium, and geckodriver beforehand to see the generation of the beats in the browser.

Important code (files):

generate.py is the python file which you can run to generate a sample of our beats. generate.py makes use of the methods and code from util.py.

util.py includes the code which includes the methods (such as using K-means, reading in inputs to get the probabilities based on our Bayesian nets) in which our algorithm resides in. 

scrapeInput.py is the python file that includes the code for scraping the urls from twitter and creating the file new_songs_data(incl. twitter). twitterscraper was used to scrape the urls from twitter. More specific details are listed in scrapeInput.py.

new_songs_data(incl. twitter) contains the input data we scraped for the algorithm.

