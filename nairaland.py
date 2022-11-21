"""
This code scrapes data from Nairaland website and formats the data into a CSV
Two folders are created in the Desktop which is Nairaland_Scraper and Nairaland_csv
The CSV file is moved from the Nairaland_Scraper folder to the Nairaland_csv
upon a prompt to name the csv file, the file name must end with '_csv' this enables the programme detect what file should be moved to the Nairaland_csv.
"""
# still under developmemt

import pandas as pd
import requests
from bs4 import BeautifulSoup
import shutil
import os
'''
#place text to pandas and csv
df = pd.DataFrame(list_text)
csv = input('Enter name of csv: ')
df.to_csv(csv) 

#move file to folder
source = "C:\\Users\\user\\Desktop\\Nairaland_Scraper"
destination = "C:\\Users\\user\\Desktop\\Nairaland_Scraper\\Nairaland_csv"

try:
    for file in os.listdir(source):
        if file.endswith('_csv'):
            shutil.move(source + f'\\{file}', destination)
            print('file moved')
            print(f"{file}")

except Exception as error:
    print(error)

'''


class NairalandScrapper(object):

    def __init__(self, search_terms):
        self.search_terms = search_terms
        self.url_structure = "https://www.nairaland.com/search/{}/0/0/0/0"
        self.soup=""

    # makes request to nairaland with the inputed search term, can currently take one worded search terms
    def get_request_content(self):
        response = requests.get(self.url_structure.format(self.search_terms))
        return response.content

    # makes the soup object for us to extract data out of
    def make_soup(self):
        page_content = self.get_request_content()
        self.soup = BeautifulSoup(page_content, 'lxml')

    # This gets the number of search pages that turn up as result, the idea is to use a for loop and turn the last
    # digit in the url link to iterate with the for loop
    def get_num_search_results(self):
        next_page_links = self.soup.p
        num_search_page_results = next_page_links.find_all('b')[-1].text
        return num_search_page_results

    # this extracts the post details on nairaland page
    def get_page_data(self):
        nairaland_stats_for_day = self.soup.table
        post_data_table = nairaland_stats_for_day.find_next_sibling("table")
        post_data_tr = post_data_table.find_all("tr")
        return post_data_tr

    # extracts time of post,
    # needs working on
    def extract_post_time(self, post_data_list):    # post headline start from 1st tr tag
        post_data = []
        post_headline_data = {}
        for post_id in range(0, len(post_data_list), 2):
            post_headline_data = {}
            # sometimes there are empty table rows in nairaland which don't have any data but the table row tag shows
            # in such situations table row data doesn't exceed 1 item with find all, so we skip the rest of code if less
            # than or equal to 1 item
            headline = post_data_list[post_id].find_all("a")
            if len(headline) <= 1:  # check if post is empty
                continue
            time = post_data_list[post_id].find('span', {'class':'s'})
            headline_tag = headline[-3::]    # the important information start from the third to last index
            headline_list = [headline.text for headline in headline_tag ]
            post_headline_data['board'] = headline_list[0]
            post_headline_data['post_title'] = headline_list[1]
            post_headline_data['posted_by_user'] = headline_list[2]
            if time:
                post_headline_data['time_of_post'] = time.text
                post_data.append(post_headline_data)
                continue
            post_headline_data['time_of_post'] = "not available"
            post_data.append(post_headline_data)
        return post_data

    # functional, would have to check for variable names later
    def extract_post_text(self, post_data_list):
        post_data = []
        for post_id in range(1, len(post_data_list), 2):    # post start from 2nd tr tag
            nairaland_user_post = {'quote': False, 'quoted_post': "", 'statistics': ""}

            post_block = post_data_list[post_id].find('div')
            print(post_id)
            quote = post_block.find('blockquote')
            if quote:
                nairaland_user_post['quote'] = True
                nairaland_user_post['quoted_post'] = quote.extract().text

            nairaland_user_post['post_text'] = post_block.text

            post_statistics_tag = post_data_list[post_id].find('p')     # likes and shares
            if post_statistics_tag:
                nairaland_user_post['statistics'] = post_statistics_tag.text

            post_data.append(nairaland_user_post)   # adding dictionaries to a list brings up issues
        return post_data



a = NairalandScrapper("chelsea")
a.make_soup()
b = a.get_page_data()
print(a.extract_post_time(b))