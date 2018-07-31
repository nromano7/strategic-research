from datetime import datetime
import logging
from pytools.webdrivers import ChromeDriver
from pytools.fileEventHandler import Watcher
import os
from random import randint
import time
import trid_xml2json

# ///// INPUTS /////
URL = r"""https://trid.trb.org/Results?
txtKeywords=&txtTitle=&txtSerial=&ddlSubject=1797&
txtReportNum=&ddlTrisfile=&txtIndex=%20&specificTerms=&
txtAgency=&txtAuthor=&ddlResultType=&chkFulltextOnly=0&
language=1&subjectLogic=or&dateStart=2006&dateEnd=2019&
rangeType=publisheddate&sortBy=&sortOrder=DESC&rpp=100"""
DOWNLOADS_DIRECTORY = r"C:/Users/Nick/Documents/Projects/LTBP/Strategic Research/data_files/"
HEADLESS = True
# ///// /////

# create downloads folder if it does not exist
now = datetime.now()
year, month, day = now.year, now.month, now.day
DOWNLOADS_FOLDER = os.path.join(DOWNLOADS_DIRECTORY,f"{year:04}{month:02}{day:02}")
XML_PATH = os.path.join(DOWNLOADS_FOLDER, "xml")
JSON_PATH = os.path.join(DOWNLOADS_FOLDER, "json")
if not os.path.isdir(DOWNLOADS_FOLDER):
  os.mkdir(DOWNLOADS_FOLDER)
  os.mkdir(XML_PATH)
  os.mkdir(JSON_PATH)
  os.mkdir(os.path.join(JSON_PATH,"projects"))
  os.mkdir(os.path.join(JSON_PATH,"publications"))

kwargs = {
  'headless': HEADLESS,
  'prompt_for_download': False,
  'download_directory': DOWNLOADS_FOLDER
}

# logging
LOGFILE_PATH = os.path.join(DOWNLOADS_DIRECTORY,f"logs/log-{year:04}{month:02}{day:02}")
logging.basicConfig(
      filename=f'{LOGFILE_PATH}.log', 
      level=logging.DEBUG,
      format='%(levelname)s:%(message)s'
    )

with Watcher(DOWNLOADS_FOLDER, log_filepath=LOGFILE_PATH):
  with ChromeDriver(**kwargs) as driver:
    
    driver.open(URL)
    count = 0

    while True:

      time_delay = randint(10,randint(10,40))
      time.sleep(time_delay)

      count += 1
      print(f'[Navigating Page {count}; Time Delay = {time_delay+10}]...')
      logging.debug(f'[Navigating Page {count}; Time Delay = {time_delay+10}]...')

      ## navigate page and download 
      js_commands = ';'.join([
          r"document.getElementById('mark-page').click()", # selects all record check boxes on current page
          r"$('#save_modal').modal('show')", # opens modal of save options
          r"document.querySelectorAll('input[value=XML]')[1].click()", # select XML button...could use driver.findelements(XPATH)
          r"document.getElementById('saveMarkedResults').click()", # clicks download button to download results
        ])
      driver.execute(js_commands)

      ## wait for download to complete
      time.sleep(10) 

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

      # rename and move downloaded file
      xml_files = [f for f in os.listdir(DOWNLOADS_FOLDER) if f.endswith(".xml")]
      if len(xml_files) > 1:
        raise Exception()
      fname = xml_files.pop().split(".")[0]
      newfname = f"{fname}_{count:03}.xml"
      src = os.path.join(DOWNLOADS_FOLDER, f"{fname}.xml")
      dst = os.path.join(XML_PATH, newfname)
      os.rename(src, dst)


  trid_xml2json.projects_xml2json(XML_PATH, JSON_PATH)
  trid_xml2json.publications_xml2json(XML_PATH, JSON_PATH)


