import time
import io

import os.path
from os import path

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium import webdriver

#TODO:
#   1. Remove useless imports, var renaming, code formatting, comments
#   2. Set from console
#           as parameters: PROFILE_ID, PAGES_COUNT, PATH
#           as flags: show logs, not headless browser
#   3. Refactoring:
#           - create c_printer (privide color print)
#           - driver_service (generate browser)
#           - soundcloud_spy(get links by profile id)
#           - sclouddownloader (download tracks by sclouddownloader)
#           - var renaming
#   4. Use local WebDriver
#   5. Create web or desktop UI

# colors
OKGREEN='\033[92m'
OKCYAN='\033[96m'
OKBLUE='\033[94m'
WARNING='\033[93m'
FAIL='\033[91m'

# start timer
start_time = time.time()

# init paramas
PATH='C:\\Users\\borbi\\Desktop\\'
FILE_ID='soundcloud_links'
PROFILE_ID='krle3gd6tuxg'
PAGES_COUNT=1
DEALEY=0.1
SMALL_WAIT=0.3
BIG_WAIT=1
LARGE_WAIT=2
DOWNLOAD_WAIT=5

# get new file name with uniqe key
fileName = f'{PATH}{FILE_ID}_for_{PROFILE_ID}'

# get browser
def getBrowser():
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", 'C:\\Users\\borbi\\Downloads\\firefox')
    fp.set_preference("privacy.popups.showBrowserMessage", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", ".mp3 audio/mpeg")

    options = Options()
    options.headless = True

    browser=webdriver.Firefox(options=options, firefox_profile=fp, service_log_path="./geckodriver.log")

    print (f'{OKBLUE}- Headless Browser Initialized{OKBLUE}')

    return browser

# get links by profile id
def links(browser, profile_id):
    links=[]

    # open page at browser
    browser.get(f'https://soundcloud.com/{profile_id}/likes')
    #browser.
    browser.maximize_window()
    time.sleep(SMALL_WAIT)

    # scroll page
    body=browser.find_element_by_tag_name('body')
    count=PAGES_COUNT
    while count:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(DEALEY)
        count-=1
    
    # add new links
    elements=browser.find_elements_by_class_name('sound__coverArt')
    for element in elements:
        link=element.get_attribute('href')
        if link.strip() and link not in links:
            links.append(link)
    links=[line.strip() for line in links]

    return links

# STABLE
def download(browser, link, number):
    try:
        print(f'proccesing track {number}')
        field=browser.find_element_by_name('sound-url')
        field.clear()
        field.send_keys(link)
        time.sleep(0.1)

        button1=browser.find_element_by_class_name('input-group-button')
        button1.click()
        time.sleep(1)

        button2=browser.find_elements_by_class_name('button')[0]
        button2.click()
        time.sleep(2)

        back=browser.find_element_by_class_name('menu')
        back.click()
        time.sleep(0.5)

    except BaseException as exception:
        printCol(f'{FAIL}error:{FAIL}\n\t{exception}')

# MAIN
browser=getBrowser()

links=links(browser, PROFILE_ID)
print(f'{OKBLUE}- {len(links)} tracks will be downloaded{OKBLUE}')

browser.get(f'https://sclouddownloader.net/')
time.sleep(SMALL_WAIT)

i = 1
for link in links:
    download(browser, link, i)
    i+=1

time.sleep(DOWNLOAD_WAIT)
browser.quit()

print(f'{OKBLUE}- Completed by {(time.time() - start_time) / 60.0} minutes ---{OKBLUE}')
