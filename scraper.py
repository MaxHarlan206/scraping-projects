import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import pandas

pandas.set_option('display.max_columns', None)
url = "https://muckrack.com/beat/food?page={}"
journalists_arr = []

def high_level():
    """ Gets the url of the main directory pages"""
    for i in range(100):
        sleep(random.randint(1, 10))
        new_url = url.format(i + 1)
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        person_names = soup.find_all('div', {'class': 'mr-directory-item'})
        for i in range(len(person_names)):
            person = person_names[i]
            person_text = person.find("a").text
            person_url = 'https://muckrack.com' + person.find("a").get('href')
            person_array = [person_text, person_url, "N/a", "N/a", "N/a"]
            write_to_csv(person_array)

def individuals():
    """ Gets name, publication, and Linkedin of each journalist"""
    data = pandas.read_csv("journalists.csv", error_bad_lines=False)
    for i in range(len(data)):
        sleep(.2)
        url = data.loc[i, "Templink"]
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #stores the name from the previoius file
        name = data.loc[i, "Name"]

        # Grabs and formats the job name
        try:
            media_outlet = soup.find('div', {'class': 'person-details-item person-details-title'})
            pos = media_outlet.text
            pos = pos.strip()
            pos = pos.replace('\n', '')
            pos = pos.replace('—', '')
            pos.rstrip()
            outlet = " ".join(pos.split())
        except:
            outlet = "None"
        # Snag LinkedIn Profile if it has one
        try:
            ln_anchor = soup.find('a', {'class': 'mr-contact break-word top-xs js-icon-linkedin mr-contact-icon-only'})
            linkedin = ln_anchor.get('href')
        except:
            linkedin = "None"

        # Gets Location
        loc_div = soup.find('div', {'class': 'person-details-item person-details-location'})
        try:
            loc = loc_div.text
            loc = loc.strip()
            loc = loc.replace('\n', '')
            loc = loc.replace('—', '')
            loc.rstrip()
            location = " ".join(loc.split())
        except:
            location = "None"

        # Update the data frame
        update_array = [name, outlet, location, linkedin]
        edit_csv(update_array)

def write_to_csv(journalist_array):
    """ Writes using Pandas data frame """
    journalists = pandas.DataFrame([journalist_array], columns=['Name',' Templink', 'Outlet', 'Location', 'LinkedIn'])
    with open('journalists.csv', 'a') as journ_file:
        journalists.to_csv(journ_file, mode='a', header=journ_file.tell()==0)

def edit_csv(journalist_detail_array):
    """ Overwrites / updates select cells in CSV """
    update_journalists = pandas.DataFrame([journalist_detail_array], columns=['Name', 'Outlet', 'Location', 'LinkedIn'])
    with open('updated_journalists.csv', 'a') as journ_file:
        update_journalists.to_csv(journ_file, mode='a', header=journ_file.tell()==0)

