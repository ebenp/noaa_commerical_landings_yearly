import scraperwiki
from splinter import Browser
#import requests
#import pandas as pd
#from bs4 import BeautifulSoup

def open_url_query_years(browser):
    '''
    Queries given url by qyear. Returns years
    :param wait: wait from WebDriverWait
    :return: list of queryable years
    '''
    # get our selector options
    select = browser.find_by_id("qyear")

    return select.text.split('\n')

def parse_table(browser,url,year):

    '''
    Parses a queried page to an HTML and dataframe
    :param wait: wait from WebDriverWait
    :param driver: Firefox Driver
    :param url: input url to query
    :param year: year to select
    :return: html, html source and table as a pandas dataframe
    '''

    browser.visit(url)
    browser.find_by_xpath("//select[@name='qyear']/option[text()=" + year + "]").click()
    browser.find_by_xpath("//input[@value='Submit Query'][@type='submit']").click()
    html = browser.html
    '''
    hp = HTMLTableParser()
    table = hp.parse_url(url, html=html, singletable=True)[0][1]  # Grabbing the table from the tuple
    '''
    return html
'''
Main script with user inputs
'''

# inputs


url = 'https://www.st.nmfs.noaa.gov/commercial-fisheries/commercial-landings' + \
      '/other-specialized-programs' + \
      '/total-commercial-fishery-landings-at-major-u-s-ports-summarized-by-year-and-ranked-by-dollar-value/index'
# processing
# set up our driver here
with Browser() as browser:
    # access the url with the driver
    browser.visit(url)
    # obtain years to access tables
    years = open_url_query_years(browser)
    # obtain and save tables in html and tab delimited text for each year desired
    for year in years:
        print(year)
        html = parse_table(browser, url, year)
        # Write out to the sqlite database using scraperwiki library
        scraperwiki.sqlite.save(unique_keys=['year'], data={"year": year, "html": html})


# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
