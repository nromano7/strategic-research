from datetime import datetime
# import logging
from webscrapper.webdrivers import ChromeDriver
from webscrapper.fileEventHandler import Watcher
from webscrapper.xml2json import xml2json
# from webdrivers import ChromeDriver
# from fileEventHandler import Watcher
# from xml2json import xml2json
import os
from random import randint
import time
import shutil

def scrape_trid(tmp_directory, downloads_folder, prev_years=1):

  now = datetime.now()
  year = now.year

  URL=("https://trid.trb.org/Results?txtKeywords=&txtTitle=&txtSerial=&ddlSubject=1797"
  "&txtReportNum=&ddlTrisfile=&txtIndex=%20&specificTerms="
  "&txtAgency=&txtAuthor=&ddlResultType=&chkFulltextOnly=0"
  "&language=1&subjectLogic=or&dateStart={}&dateEnd={}"
  "&rangeType=publisheddate&sortBy=&sortOrder=DESC&rpp=100")
  URL = URL.format(year-prev_years, year+10)

  XML_PATH = os.path.join(downloads_folder, "xml")
  JSON_PATH = os.path.join(downloads_folder, "json")

  # HEADLESS = True
  # kwargs = {
  #   'headless': HEADLESS,
  #   'prompt_for_download': False,
  #   'download_directory': downloads_folder
  # }

  # # logging
  # LOGFILE_PATH = os.path.join(tmp_directory,f"logs/log-{year:04}{month:02}{day:02}")
  # if not os.path.isdir(os.path.join(tmp_directory,"logs")):
  #   os.makedirs(os.path.join(tmp_directory,"logs"))

  # logging.basicConfig(
  #       filename=f'{LOGFILE_PATH}.log', 
  #       level=logging.DEBUG,
  #       format='%(levelname)s:%(message)s'
  #     )

  with Watcher(downloads_folder):
    with ChromeDriver(download_directory = downloads_folder) as driver:
     
      driver.open(URL)
      count = 0

      while True:

        time_delay = randint(5,randint(5,20))
        time.sleep(time_delay)

        count += 1
        print(f'[Navigating Page {count}; Time Delay = {time_delay+5}]...')
        # logging.debug(f'[Navigating Page {count}; Time Delay = {time_delay+5}]...')

        ## navigate page and download 
        js_commands = ';'.join([
            r"document.getElementById('mark-page').click()", # selects all record check boxes on current page
            r"$('#save_modal').modal('show')", # opens modal of save options
            r"document.querySelectorAll('input[value=XML]')[1].click()", # select XML button...could use driver.findelements(XPATH)
            r"document.getElementById('saveMarkedResults').click()", # clicks download button to download results
          ])
        driver.execute(js_commands)

        ## wait for download to complete
        time.sleep(5) 

        # rename and move downloaded file
        xml_files = [f for f in os.listdir(downloads_folder) if f.endswith(".xml")]
        if len(xml_files) > 1:
          raise Exception()
        fname = xml_files.pop().split(".")[0]
        newfname = f"{fname}_{count:03}.xml"
        src = os.path.join(downloads_folder, f"{fname}.xml")
        dst = os.path.join(XML_PATH, newfname)
        os.rename(src, dst)

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

      # convert xml to json
      xml2json(XML_PATH, JSON_PATH)

if __name__ == '__main__':
  scrape_trid()

        

    
    


