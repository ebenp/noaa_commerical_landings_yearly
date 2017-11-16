# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from splinter import Browser
# html table parser modified from github
# modified from http://srome.github.io/Parsing-HTML-Tables-in-Python-with-BeautifulSoup-and-pandas/
# credits to Scott Rome.
class HTMLTableParser:
    def parse_url(self, url, html=None, singletable=True):

        if html is not None:
            page = html
        else:
            response = requests.get(url)
            page = response.text


        soup = BeautifulSoup(page,'lxml')
        # updated table ID to index
        if singletable:
            return [(table.index, self.parse_html_table(table)) \
                    for table in soup.find_all('table')]
        else:
            return [(table[tableid], self.parse_html_table(table)) \
                    for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df

def open_url_query_years(browser):
    '''
    Queries given url by qyear. Returns years
    :param wait: wait from WebDriverWait
    :return: list of queryable years
    '''
    # get our selector options
    select = browser.find_by_id("qyear")

    return select

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
    hp = HTMLTableParser()
    table = hp.parse_url(url, html=html, singletable=True)[0][1]  # Grabbing the table from the tuple

    return html, table
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
        html, df = parse_table(browser url, year)
        # Write out to the sqlite database using scraperwiki library
        scraperwiki.sqlite.save(unique_keys=['year'], data={"year": year, "html": html,"dataframe":df})
    
# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
