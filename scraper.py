#!/usr/bin/env python
"""Provides scraping functionality for commercial landings page. Uses headless PhantomJS
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
# html table parser modified from github
from htmltableparser import HTMLTableParser

def open_url_query_years(wait):
    '''
    Queries given url by qyear. Returns years
    :param wait: wait from WebDriverWait
    :return: list of queryable years
    '''
    # get our selector options
    select = Select(wait.until(expected.visibility_of_element_located((By.ID,"qyear"))))

    return [o.text for o in select.options]

def parse_table(wait,driver,url,year):

    '''
    Parses a queried page to an HTML and dataframe
    :param wait: wait from WebDriverWait
    :param driver: Firefox Driver
    :param url: input url to query
    :param year: year to select
    :return: html, html source and table as a pandas dataframe
    '''

    driver.get(url)
    wait.until(expected.visibility_of_element_located((By.XPATH,"//select[@name='qyear']/option[text()=" + year + "]"))).click()
    wait.until(expected.visibility_of_element_located((By.XPATH, "//input[@value='Submit Query'][@type='submit']"))).click()
    html = driver.page_source
    hp = HTMLTableParser()
    table = hp.parse_url(url, html=html, singletable=True)[0][1]  # Grabbing the table from the tuple

    return html, table

def save_html_text(html,df,outpath,year):

    '''
    Saves table to html and text files.

    :param html: html source as string to save
    :param df: dataframe of able to save
    :param outpath: path to directory to save html and text files. The year is appended here
    :param year: year label for file names
    :return: None
    '''

    df.to_csv(outpath+r'//'+year+'.txt', sep='\t',index=False)
    with open(outpath+r'//'+year+'.html', "w") as file:
        file.write(html)
    return

if __name__ == '__main__':

    '''
    Main script with user inputs
    '''

    # inputs
    url = 'https://www.st.nmfs.noaa.gov/commercial-fisheries/commercial-landings' + \
          '/other-specialized-programs' + \
          '/total-commercial-fishery-landings-at-major-u-s-ports-summarized-by-year-and-ranked-by-dollar-value/index'
    output_dir='/Users/eben/Documents/GitHub/scraping_landings_data/text_output'

    # processing
    # set up our driver here
    options = Options()
    run = 'local'
    # Morph.io exacutable path
    if run == 'morph':
        execut_path='/usr/bin/phantomjs'
    else:
        execut_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(executable_path=execut_path,service_args=['--web-security=no',
                                               '--ssl-protocol=any', '--ignore-ssl-errors=yes'])
    # set up wait
    wait = WebDriverWait(driver, timeout=10)
    # access the url with the driver
    driver.get(url)
    # obtain years to acess tables
    years = open_url_query_years(wait)
    # obtain and save tables in html and tab delimited text for each year desired
    for year in years:
        print(year)
        html, df = parse_table(wait, driver, url, year)
        save_html_text(html, df, output_dir,year)

    # Print completion
    print('DONE!')
