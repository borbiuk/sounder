import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from selenium import webdriver

#TODO:
#   1. Set from console
#           as parameters: PROFILE_ID, PAGES_COUNT, PATH
#           as flags: show logs, not headless browser
#   2. Refactoring:
#           - create c_printer (privide color print)
#           - driver_service (generate browser)
#           - soundcloud_spy(get links by profile id)
#           - sclouddownloader (download tracks by sclouddownloader)
#           - var renaming
#   3. Use local WebDriver
#   4. Create web or desktop UI

# constants
PROFILE_ID='krle3gd6tuxg'
PAGES_COUNT=1
FIREFOX_LOGS_PATH='./geckodriver.log'
OKGREEN='\033[92m'
OKCYAN='\033[96m'
OKBLUE='\033[94m'
WARNING='\033[93m'
FAIL='\033[91m'

# returns configured browser
def get_browser():
    fp = webdriver.FirefoxProfile()

    # set preference to avoid Firefox pop-ups
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", 'C:\\Users\\borbi\\Downloads\\firefox')
    fp.set_preference("privacy.popups.showBrowserMessage", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", ".mp3 audio/mpeg")

    # set driver options torun headless browser
    op = Options()
    op.headless = True

    browser=webdriver.Firefox(options=op, firefox_profile=fp, service_log_path=FIREFOX_LOGS_PATH)

    return browser

# get links by profile id
def profile_links(browser, profile_id, pages_count):
    links=[]

    # open soundcloud profile liked tracks page at web browser
    browser.get(f'https://soundcloud.com/{profile_id}/likes')
    browser.maximize_window()
    time.sleep(0.3)

    # scroll page down
    body=browser.find_element_by_tag_name('body')
    i = pages_count
    while i:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        i-=1
    
    # get links from hml
    elements=browser.find_elements_by_class_name('sound__coverArt')
    for element in elements:
        link=element.get_attribute('href')
        links.append(link)

    return links

# download track by link from https://sclouddownloader.net/
def download_tracks(browser, links):
    errors=[]

    # open download service at browser
    browser.get(f'https://sclouddownloader.net/')
    time.sleep(0.3)
    for number, link in enumerate(links):
        try:
            # set url at input
            field=browser.find_element_by_name('sound-url')
            field.clear()
            field.send_keys(link)
            time.sleep(0.1)

            # click download button
            button1=browser.find_element_by_class_name('input-group-button')
            button1.click()
            time.sleep(1)

            # click download button on /download-sound-track page
            button2=browser.find_elements_by_class_name('button')[0]
            button2.click()
            time.sleep(2)

            # return to the main page
            back=browser.find_element_by_class_name('menu')
            back.click()
            time.sleep(0.5)

        except BaseException as exception:
            errors.append(number, exception)

    return errors

# script
browser=get_browser()

links=profile_links(browser, PROFILE_ID, 10)

download_tracks(browser, links)

time.sleep(5)

browser.quit()

print(f'{len(links)} tracks completed')