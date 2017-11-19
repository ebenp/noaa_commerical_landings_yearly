from splinter import Browser

with Browser("phantomjs") as browser:
    # Optional, but make sure large enough that responsive pages don't
    # hide elements on you...
    browser.driver.set_window_size(1280, 1024)

    # Open the page you want...
    browser.visit("https://morph.io")

    # submit the search form...
    browser.fill("q", "parliament")
    button = browser.find_by_css("button[type='submit']")
    button.click()

    # Scrape the data you like...
    links = browser.find_by_css(".search-results .list-group-item")
    for link in links:
        print(link['href'])