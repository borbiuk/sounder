import getopt, sys, time, os, argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

#TODO:
#   1. Set from console
#           as parameters: soundcloud profie_id, pages count to scroll, path to download
#           as flags: headless browser
#   2. Refactoring:
#           - create c_printer (privide color print)
#           - driver_service (generate browser)
#           - soundcloud_spy(get links by profile id)
#           - sclouddownloader (download tracks by sclouddownloader)
#           - var renaming
#   3. Use local WebDriver
#   4. Create web or desktop UI

profie_id='krle3gd6tuxg'
pages_count=1
download_path=''
headless_mode=False

# constants
FIREFOX_LOGS_PATH='./geckodriver.log'
DELAY=0.5
WAIT=2
OKGREEN='\033[92m'
OKCYAN='\033[96m'
OKBLUE='\033[94m'
WARNING='\033[93m'
FAIL='\033[91m'

# returns configured browser
def get_browser(download_path, headless):
    fp = webdriver.FirefoxProfile()

    # set preference to avoid Firefox pop-ups
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_path)
    fp.set_preference("privacy.popups.showBrowserMessage", False)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", ".mp3 audio/mpeg")

    # set driver options to run headless browser
    op = Options()
    if headless:
        op.headless = True

    browser=webdriver.Firefox(options=op, firefox_profile=fp, service_log_path=FIREFOX_LOGS_PATH)

    return browser

# get links by profile id
def profile_links(browser, profile_id, pages_count):
    links=[]

    # open soundcloud profile liked tracks page at web browser
    browser.get(f'https://soundcloud.com/{profile_id}/likes')
    browser.maximize_window()
    time.sleep(DELAY)

    # scroll page down
    body=browser.find_element_by_tag_name('body')
    i = pages_count
    while i:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(DELAY)
        i-=1
    
    # get links from html
    elements=browser.find_elements_by_class_name('sound__coverArt')
    for element in elements:
        link=element.get_attribute('href')
        links.append(link)

    return links

# download track by link from https://sclouddownloader.net/
def download_tracks(browser, links):
    completed=0

    # open download service at browser
    browser.get(f'https://sclouddownloader.net/')
    time.sleep(DELAY)
    for number, link in enumerate(links):
        try:
            print(f'{OKBLUE}\t- track {number} Processing...\n\t  [{link}]{OKBLUE}')
            # set url at input
            field=browser.find_element_by_name('sound-url')
            field.clear()
            field.send_keys(link)
            time.sleep(DELAY)

            # click download button
            button1=browser.find_element_by_class_name('input-group-button')
            button1.click()
            time.sleep(DELAY)

            # click download button on /download-sound-track page
            button2=browser.find_elements_by_class_name('button')[0]
            button2.click()
            time.sleep(WAIT)

            # return to the main page
            back=browser.find_element_by_class_name('menu')
            back.click()
            time.sleep(DELAY)

            completed+=1
            print(f'{OKGREEN}\t  track {number} Completed{OKGREEN}')
        except BaseException as error:
            print(f'{FAIL}Error was throw when track {number} downloding [{link}]\n\t{str(error)}{FAIL}')

    return completed

# script
try:
    if download_path == '':
        download_path=f'{os.getcwd()}'
    browser=get_browser(download_path, headless_mode)

    print(f'{OKCYAN}Your tracks searching in the process ...{OKCYAN}')

    links=profile_links(browser, profie_id, pages_count)
    links_count=len(links)

    print(f'{OKCYAN}Found {links_count} tracks. Downloading in the process...{OKCYAN}')

    completed=download_tracks(browser, links)

    print(f'{OKCYAN}{completed} from {links_count} tracks was completed!{OKCYAN}')

    time.sleep(2)
    browser.close()
except BaseException as error:
    print(f'{FAIL}Programm error was throw:\n\t{str(error)}{FAIL}')