from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

#Defining the web driver for selenium
driver = webdriver.Chrome("/home/max/Documents/chromedriver")
driver.set_window_size(500,700)
#assigning a variable for quotes dictionary keys
quotes_dict_pos = 1 
quotes_dict = {}

def scrape_quotes(self):
	"""Takes a page url, adds an index number and text to a dictionary for posts of a certain class"""
	driver.get(self)
	quotes = driver.find_elements_by_class_name("quoteText")
	global quotes_dict
	global quotes_dict_pos
	for q in range(len(quotes)):
		quotes_dict[quotes_dict_pos] = quotes[q].text
		print(f'{quotes_dict[quotes_dict_pos]}: {quotes[q].text}')
		quotes_dict_pos += 1

#Iterates through page urls and calls the quote scraping function on each page
for page in range(1,21):
	if page == 1:
		scrape_quotes("WEBSITE/quotes/tag/writing")
	else:
		page_num = "?page="+str(page)
		url = "WEBSITE/quotes/tag/writing/"+page_num
		scrape_quotes(url)

with open('writing_quotes.json', 'w') as json_file:
  json.dump(quotes_dict, json_file) 
