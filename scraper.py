from splinter import Browser
import sys, shutil

dev_mode = True

with Browser("phantomjs") as browser:
    # Optional, but make sure large enough that responsive pages don't
    # hide elements on you...
    browser.driver.set_window_size(1280, 1024)

    # Open the page you want...
    browser.visit("https://morph.io")

    if dev_mode:
        browser.screenshot('screen_0001.png')  # save a screenshot to disk

    # submit the search form...
    browser.fill("q", "parliament")
    button = browser.find_by_css("button[type='submit']")
    button.click()

    if dev_mode is True:
        with open("ghostdriver.log", "r") as f:
            shutil.copyfileobj(f, sys.stdout)

    # Scrape the data you like...
    links = browser.find_by_css(".search-results .list-group-item")
    for link in links:
        print(link['href'])