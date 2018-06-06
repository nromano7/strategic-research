from webdrivers import ChromeDriver
import time
from random import randint

# TODO: fix issue with wait_for method

URL = r"https://trid.trb.org/Results?txtKeywords=&ddlSubject=1797&ddlTrisfile=&rpp=100"
DOWNLOAD_DIRECTORY = r"C:\Users\Nick\Downloads\Test"
HEADLESS = False

kwargs = {
  'headless': HEADLESS,
  'download_directory': DOWNLOAD_DIRECTORY
}

with ChromeDriver(**kwargs) as driver:
  
  driver.open(URL)

  while True:

    time_delay = randint(10,20)
    time.sleep(time_delay)

    ## navigate page and download 
    js_commands = ';'.join([
        r"document.getElementById('mark-page').click()", # selects all record check boxes on current page
        r"$('#save_modal').modal('show')", # opens modal of save options
        r"document.querySelectorAll('input[value=XML]')[1].click()", # select XML button...could use driver.findelements(XPATH)
        r"document.getElementById('saveMarkedResults').click()", # clicks download button to download results
      ])
    driver.execute(js_commands)

    ## wait for download to complete
    time.sleep(10) # driver.wait_for('download_complete')

    ## clear selections and navigate to next page
    visibility = driver.execute(r"return $('.record-pagination-forward').css('visibility')") # check if there is a next page
    if visibility == 'visible':
      js_commands = ';'.join([
        r"document.getElementById('mark-clear').click()", # deselects all
        r"document.getElementsByClassName('record-pagination-forward')[0].click()", # goes to next page
      ])
      driver.execute(js_commands)
    elif visibility == 'hidden': # there is no next page
      break
