from datetime import datetime
import json
from lxml import etree

# TODO: write to xml and csv

file = './files/raw/TRIDXML_2018-06-06.xml'

# parse xml document
parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
tree = etree.parse(file,parser)

# get all project records in the current file
project_records_xml = tree.xpath("./record[@type='project']")

record = {}

for xml_record in project_records_xml:

  ## get data and store to record dict 

  # title
  record['title'] = ' '.join(xml_record.findtext("title").split())

  # abstract
  record['abstract'] = ' '.join(xml_record.findtext("abstract") \
    .replace('\n','').split()).replace("\u00ef\u00bf\u00bd",'') # clean up

  # notes
  notes = xml_record.findtext('supplemental_notes')
  record['notes'] = notes.replace('\n','').replace('  ',' ') if notes else str() # clean up
 
  # urls
  record['urls'] = [url.text for url in xml_record.xpath("./document_urls/*")]

  # status
  record['status'] = xml_record.xpath("./project/project_status")[0].text

  # # funding
  # TODO: fix formatting of funding
  # funding = xml_record.xpath("./project/funding")[0].text
  # record['funding'] = 0.0 if not funding else float(funding.replace(',','').replace('$',''))

  # start date
  # TODO: handle when no date is available
  # start_date = xml_record.xpath("./project/start_date")[0].text
  # start_date = "0000-00-00" if (start_date == '0') \
  #  or (start_date is None) \
  #  else datetime.strptime(start_date,'%Y%m%d').isoformat()[0:10]
  # record['start'] = start_date

  # # expected completion date
  # TODO: handle when no date is available
  # expected_complete = xml_record.xpath("./project/expected_completion_date")[0].text
  # expected_complete = str() if (expected_complete == '0') or \
  #  (expected_complete is None) \
  #  else datetime.strptime(expected_complete,'%Y%m%d').isoformat()[0:10]
  # record['expected_complete'] = expected_complete
 
  # # actual completion date
  # TODO: handle when no date is available
  # actual_complete = xml_record.xpath("./project/actual_completion_date")[0].text
  # actual_complete = str() if (actual_complete == '0') or \
  #  (actual_complete is None) \
  #  else datetime.strptime(actual_complete,'%Y%m%d').isoformat()[0:10]
  # record['actual_complete'] = actual_complete

  with open(f'./files/transformed/json/TRID_{xml_record.attrib["id"]}.json', 'w') as f:
    json.dump(record, f)





  
  

  
  

  

  

  


  
