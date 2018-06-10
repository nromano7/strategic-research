from webdrivers import ChromeDriver
import time
from random import randint

# TODO: fix issue with wait_for method

URL = r"https://trid.trb.org/Results?txtKeywords=(bridge%20OR%20bridges)%20NOT%20rail*&txtTitle=&txtSerial=&ddlSubject=&txtReportNum=&ddlTrisfile=&txtIndex=%20&specificTerms=&txtAgency=&txtAuthor=&ddlResultType=&chkFulltextOnly=0&language=1&subjectLogic=or&dateStart=201306&dateEnd=201809&rangeType=recordcreateddate&sortBy=&sortOrder=DESC&rpp=100"
DOWNLOAD_DIRECTORY = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608"
HEADLESS = False

kwargs = {
  'headless': HEADLESS,
  'download_directory': DOWNLOAD_DIRECTORY
}

with ChromeDriver(**kwargs) as driver:
  
  driver.open(URL)
  count = 0

  while True:

    time_delay = randint(10,randint(20,60))
    time.sleep(time_delay)

    count += 1
    print(f'[Navigating Page {count}; Time Delay = {time_delay+10}]...')

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
      print('Done.\n')
    elif visibility == 'hidden': # there is no next page
      break
