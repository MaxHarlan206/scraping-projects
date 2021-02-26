import requests
from bs4 import BeautifulSoup
from time import sleep
import random
# Pandas would be needed if you were to write to CSV, XLSX, or SQL. DO NOT REMOVE
# import pandas

"""
This project was built to demonstrate more complex scraping techniques. 
Don't use this script to scrape Yelp. They will ban you. 
"""


def run_program():
    search_criteria()
    search_iterate()


def search_criteria():
    """ Requests search input, returns formatted global variables """
    global search_term
    global location

    raw_search_term = input("What would you like to find?")
    split_search = raw_search_term.split(" ")
    if len(split_search) > 1:
        search_term = "+".join(split_search)
    else:
        search_term = raw_search_term
    raw_location = input("What city would you like to search in?")
    split_location = raw_location.split(" ")
    if len(split_location) > 1:
        location = "+".join(split_location)
    else:
        location = raw_location


def search_iterate():
    """ Iterates over the main search results pages """
    next_arrow = 1
    idx = 0
    while next_arrow is not None:
        sleep(random.randint(1, 5))
        # initialize the basic soup object
        url = "https://www.yelp.com/search?find_desc={}&find_loc={}&start={}".format(search_term, location, idx)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # for each business in the soup, run the get business details function
        business_link_divs = soup.find_all('a', {'class': 'css-166la90'})
        for biz_link in business_link_divs[:10]:
            end_biz_url = biz_link.get('href')
            biz_url = "https://yelp.com"+end_biz_url
            get_biz_details(biz_url)

        # set things up for the next iteration through... or not.
        try:
            next_arrow = soup.find('a', {'class': 'next-link navigation-button__09f24__3F7Pt css-166la90'})
        except:
            next_arrow = None
        idx += 10


def get_biz_details(biz_url):
    """ Pulls all relevant details off of business listing pages """
    global biz_name
    global star_rating
    global date_rows
    global business_url
    global biz_number
    global biz_address_formatted

    sleep(random.randint(1, 5))

    page = requests.get(biz_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # BUSINESS NAME
    try:
        biz_name = soup.find('h1', {'class': 'heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy'}).text
    except:
        biz_name = None

    # BUSINESS RATING
    try:
        star_rating = soup.find('div', {'class':'i-stars__373c0__1BRrc i-stars--large-5__373c0__VWKG_ border-color--default__373c0__3-ifU overflow--hidden__373c0__2y4YK'}).get('aria-label')[0]
    except:
        star_rating = None

    # BUSINESS HOURS
    try:
        date_rows = soup.find_all('tr', {'class': 'table-row__373c0__3wipe'})
        for date_row in date_rows:
            if len(date_row) > 0:
                formatted_date = date_row.text.replace('Open now', '')
    except:
        formatted_date = None

    # BUSINESS URL
    try:
        biz_link = soup.find('a', {'class':'link__373c0__1G70M link-color--blue-dark__373c0__85-Nu link-size--inherit__373c0__1VFlE'}).get('href')
        business_url = requests.get("https://yelp.com"+biz_link).text
    except:
        business_url = None

    # BUSINESS NUMBER
    try:
        biz_numbers = soup.find_all('p', {'class': 'text__373c0__2Kxyz text-color--normal__373c0__3xep9 '
            'text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-size--large__373c0__3t60B'})
        biz_number = biz_numbers[2].text
    except:
        biz_number = None

    # BUSINESS ADDRESS
    try:
        biz_address = soup.find('div', {'class':  'arrange-unit__373c0__o3tjT arrange-unit-fill__373c0__3Sfw1 '
                                                  'border-color--default__373c0__3-ifU'})
        biz_address_soup = BeautifulSoup(biz_address, 'html.parser')
        biz_add_parts = biz_address_soup.find_all("p")
        final_biz_address = []
        for biz_add in biz_add_parts:
            final_biz_address.append(biz_add.text)
        biz_address_formatted = " ".join(final_biz_address)
    except:
        biz_address_formatted = None

    data_to_csv()


def data_to_csv():
    """ Here is where you would create a pandas dataframe
    and then write to your storage medium of choice.
    But don't do that ;) it'll get your I.P. banned from Yelp"""
    pass
