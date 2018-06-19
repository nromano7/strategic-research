from datetime import datetime
import json
from lxml import etree

# TODO: write to xml and csv

file = './files/test_files/raw/TRIDXML_2018-06-06.xml'

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
  record['notes'] = notes.replace('\n','').replace('  ',' ') if notes else None # clean up
 
  # urls
  record['urls'] = [url.text for url in xml_record.xpath("./document_urls/*")]

  # status
  record['status'] = xml_record.xpath("./project/project_status")[0].text

  # funding
  funding = xml_record.xpath("./project/funding")[0].text
  record['funding'] = None if funding is None else float(funding.replace(',','').split('$')[-1])

  # start date
  start_date = xml_record.xpath("./project/start_date")[0].text
  record['start'] = None if start_date is '0' else datetime.strptime(start_date,'%Y%m%d').isoformat()[0:10]

  # expected completion date
  expected_complete = xml_record.xpath("./project/expected_completion_date")[0].text
  record['expected_complete'] = None if expected_complete is '0' else datetime.strptime(expected_complete,'%Y%m%d').isoformat()[0:10]

  # actual completion date
  actual_complete = xml_record.xpath("./project/actual_completion_date")[0].text
  record['actual_complete'] = None if actual_complete is '0' else datetime.strptime(actual_complete,'%Y%m%d').isoformat()[0:10]

  # performing agencies
  record['performing_agencies'] = []
  for perf_agency in xml_record.xpath("./project/performing_agencies/*"):
    agency = {}
    agency['name'] = perf_agency.text
    agency['city'] = perf_agency.attrib['city'] if 'city' in perf_agency.attrib else str()
    agency['state'] = perf_agency.attrib['region'] if 'region' in perf_agency.attrib else str()
    agency['country'] = perf_agency.attrib['country_name'] if 'country_name' in perf_agency.attrib else str()
    agency['postal_code'] = perf_agency.attrib['postal_code'] if 'postal_code' in perf_agency.attrib else str()
    agency['site_url'] = perf_agency.attrib['site_url'] if 'site_url' in perf_agency.attrib else str()
    record['performing_agencies'].append(agency)

  # funding agencies
  record['funding_agencies'] = []
  for fund_agency in xml_record.xpath("./project/funding_agencies/*"):
    agency = {}
    agency['name'] = fund_agency.text
    agency['city'] = fund_agency.attrib['city'] if 'city' in fund_agency.attrib else str()
    agency['state'] = fund_agency.attrib['region'] if 'region' in fund_agency.attrib else str()
    agency['country'] = fund_agency.attrib['country_name'] if 'country_name' in fund_agency.attrib else str()
    agency['postal_code'] = fund_agency.attrib['postal_code'] if 'postal_code' in fund_agency.attrib else str()
    agency['site_url'] = fund_agency.attrib['site_url'] if 'site_url' in fund_agency.attrib else str()
    record['funding_agencies'].append(agency)

  # managing agencies
  record['managing_agencies'] = []
  for manage_agency in xml_record.xpath("./project/manager_agencies/*"):
    agency = {}
    agency['name'] = manage_agency.text
    agency['city'] = manage_agency.attrib['city'] if 'city' in manage_agency.attrib else str()
    agency['state'] = manage_agency.attrib['region'] if 'region' in manage_agency.attrib else str()
    agency['country'] = manage_agency.attrib['country_name'] if 'country_name' in manage_agency.attrib else str()
    agency['postal_code'] = manage_agency.attrib['postal_code'] if 'postal_code' in manage_agency.attrib else str()
    agency['site_url'] = manage_agency.attrib['site_url'] if 'site_url' in manage_agency.attrib else str()
    record['managing_agencies'].append(agency)

  # project investigators
  record['project_investigators'] = []
  for investigator in xml_record.xpath("./project/investigators/*"):
    individual = {}
    individual['firstname'] = investigator.attrib['firstname']
    individual['lastname'] = investigator.attrib['lastname']
    record['project_investigators'].append(individual)

  # responsible individuals
  record['responsible_individuals'] = []
  for resp_individual in xml_record.xpath("./project/responsible_individuals/*"):
    individual = {}
    individual['firstname'] = resp_individual.attrib['firstname']
    individual['lastname'] = resp_individual.attrib['lastname']
    record['responsible_individuals'].append(individual)

  # TRID meta data 
  record['TRID_RECORD_BASE'] = xml_record.base
  record['TRID_RECORD_ID'] = xml_record.attrib['id']
  record['TRID_RECORD_TYPE'] = xml_record.attrib['type']
  record['TRID_TRIS_FILE_CODES'] = [code.text for code in xml_record.xpath("./tris_files/*")]
  record['TRID_INDEX_TERMS'] = [term.text for term in xml_record.xpath("./index_terms/*")]
  record['TRID_SUBJECT_AREAS'] = [subject.text for subject in xml_record.xpath("./subject_areas/*")]

  with open(f'./files/test_files/transformed/json/TRID_{xml_record.attrib["id"]}.json', 'w') as f:
    json.dump(record, f, indent = 2)





  
  

  
  

  

  

  


  
