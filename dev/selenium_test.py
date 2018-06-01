from contextlib import contextmanager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pytools.ContextManagers.timer import timer
import time

from selenium.webdriver.support.ui import WebDriverWait

URL = r"https://trid.trb.org/Results?txtKeywords=&ddlSubject=1797&ddlTrisfile=&rpp=25"

@contextmanager
def ChromeWebDriver(headless=True):
  CHROME_DRIVER_EXECUTABLE = r"C:\Program Files (x86)\Chrome Driver\chromedriver.exe"
  options = Options()
  options.set_headless(headless=headless)
  prefs = {
    "download.default_directory": r"C:\Users\Nick\Downloads\Test",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
  }
  options.add_experimental_option("prefs", prefs)
  driver = webdriver.Chrome(
    options=options, executable_path=CHROME_DRIVER_EXECUTABLE)
  yield driver
  driver.quit()

def download_complete(driver):
  last_url = driver.current_url
  if not driver.current_url.startswith("chrome://downloads"):
    driver.get("chrome://downloads/")
    js_commands = [
      r"var items = downloads.Manager.get().items_",
      r"if (items.every(e => e.state === 'COMPLETE')) {return items.map(e => e.file_url)}"
    ]
    script = ';'.join(js_commands)
    paths = driver.execute_script(script)
  driver.get(last_url)
  return paths


with timer('js injection'):
  with ChromeWebDriver(headless=False) as driver:
     
    ## navigate page and download 
    js_commands = [
      r"document.getElementById('mark-page').click()", # selects all record check boxes on current page
      r"$('#save_modal').modal('show')", # opens modal of save options
      r"document.querySelectorAll('input[value=XML]')[1].click()", # select XML button...could use driver.findelements(XPATH)
      r"document.getElementById('saveMarkedResults').click()", # clicks download button to download results
    ]
    script = ';'.join(js_commands)
    driver.get(URL)
    driver.execute_script(script)
    paths = WebDriverWait(driver, 120, 1).until(download_complete) # waits for all the files to be completed and returns the paths
    
    ## clear selections and navigate to next page
    js_commands = [
      r"document.getElementById('mark-clear').click()", # deselects all
      r"document.getElementsByClassName('record-pagination-forward')[0].click()", # goes to next page
    ]
    script = ';'.join(js_commands)
    driver.execute_script(script)
    

# TODO:
# - implement 'page object pattern' with logging
# 	- context manager may be implmented in the page object
# - implement implicit wait for random wait times


"""
# initial testing of driving chrome for a google search

with timer('simple chrome driver test'):
    with ChromeWebDriver(headless=False) as driver:
        driver.get("https://www.google.com/")
        assert "Google" in driver.title
        print(driver.title)
        search_box = driver.find_element_by_name('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
"""
