from datetime import datetime
import json
from lxml import etree
from os import listdir, path

XML_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\raw"
JSON_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\projects"

def projects_xml2json(XML_PATH, JSON_PATH):

  all_xml_files = listdir(XML_PATH)

  def fundingCheck(x):
    try:
      float(x)
      return float(x)
    except ValueError:
      return None

  def dateCheck(x):
    try:
      date = datetime.strptime(x,'%Y%m%d').isoformat()[0:10]
      return date
    except ValueError:
      if x[-4:] == '0000':
        date = datetime.strptime(x[:-4]+'0101','%Y%m%d').isoformat()[0:10]
        return date
      if x[-2:] == '00':
        date = datetime.strptime(x[:-2]+'01','%Y%m%d').isoformat()[0:10]
        return date

  def fixStateName(x):
    if x is None:
      return x
    x = x.lower()
    with open('./files/states.csv','r', encoding='utf-8-sig') as f:
      states = {}
      for line in f:
        name, abbrv = line.replace('\n','').split(',')
        states[abbrv.lower()] = (name.lower(), abbrv.lower())
    state, abbrv = states.get(x, [x, None])
    if abbrv:
      return abbrv.upper()
    else:
      for state, abbrv in states.values():
        if x == state:
          return abbrv.upper()
      else:
        print(x)
        raise(Exception)

  def agencyCheck(x):

    agency = {
      'name': x.text,
      'city': x.attrib.get('city'),
      'state': x.attrib.get('region'),
      'country': x.attrib.get('country_name'),
      'postal_code': x.attrib.get('postal_code'),
      'site_url': x.attrib.get('site_url')
    }

    try: # sometimes postal code, region (state), and city are swapped
      # if region (state) and postal_code are swapped
      agency['postal_code'] = int(x.attrib['region']) 
      agency['state'] = None
      # if city and region (state) are swapped
      if agency.get('city') and (len(agency['city']) == 2) and agency['city'].isupper():
        agency['state'] = agency['city']
        agency['city'] = None
      return agency
    except:
      # if city and region (state) are swapped
      if agency.get('city') and (len(agency['city']) == 2) and agency['city'].isupper():
        agency['state'] = agency['city']
        agency['city'] = None
      return agency
    
        
  for xml_file in all_xml_files:

    file = path.join(XML_PATH, xml_file)

    # parse xml document
    parser = etree.XMLParser(ns_clean=True, remove_blank_text=True, recover=True)
    tree = etree.parse(file,parser)

    # get all project records in the current file
    project_records_xml = tree.xpath("./record[@type='project']")

    record = {}

    for xml_record in project_records_xml:

      ## get data and store to record dict 

      record['type'] = 'project'

      # title
      record['title'] = ' '.join(xml_record.findtext("title").split())

      # abstract
      record['abstract'] = ' '.join(xml_record.findtext("abstract") \
        .replace('\n','').split()).replace("\u00ef\u00bf\u00bd",'') # clean up

      # notes
      notes = xml_record.findtext('supplemental_notes')
      record['notes'] = notes.replace('\n','').replace('  ',' ') if notes else None # clean up
    
      # urls
      record['urls'] = []
      record['urls'] = [url.text for url in xml_record.xpath("./document_urls/*")]
      
      # status
      record['status'] = xml_record.xpath("./project/project_status")[0].text

      # funding
      funding = xml_record.xpath("./project/funding")[0].text
      record['funding'] = None if funding is None else fundingCheck(funding.replace(',','').split('$')[-1])

      # start date
      start_date = xml_record.xpath("./project/start_date")[0].text
      record['start_date'] = None if start_date is '0' else dateCheck(start_date)

      # expected completion date
      expected_complete = xml_record.xpath("./project/expected_completion_date")[0].text
      record['expected_complete_date'] = None if expected_complete is '0' else dateCheck(expected_complete)

      # actual completion date
      actual_complete = xml_record.xpath("./project/actual_completion_date")[0].text
      record['actual_complete_date'] = None if actual_complete is '0' else dateCheck(actual_complete)

      # performing agencies
      record['performing_agencies'] = []
      for perf_agency in xml_record.xpath("./project/performing_agencies/*"):
        agency = agencyCheck(perf_agency)
        agency['state'] = fixStateName(agency.get('state'))
        record['performing_agencies'].append(agency)

      # funding agencies
      funding_agencies = xml_record.xpath("./project/funding_agencies/*")
      record['funding_agencies'] = []
      for fund_agency in funding_agencies:
        agency = agencyCheck(fund_agency)
        agency['state'] = fixStateName(agency.get('state'))
        record['funding_agencies'].append(agency)

      # managing agencies
      record['managing_agencies'] = []
      for manage_agency in xml_record.xpath("./project/manager_agencies/*"):
        agency = agencyCheck(manage_agency)
        agency['state'] = fixStateName(agency.get('state'))
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

      # tags
      record['tags'] = []

      # TRID meta data 
      record['TRID_RECORD_BASE'] = xml_record.base
      record['TRID_RECORD_ID'] = xml_record.attrib['id']
      record['TRID_RECORD_TYPE'] = xml_record.attrib['type']
      record['TRID_TRIS_FILE_CODES'] = [code.text for code in xml_record.xpath("./tris_files/*")]
      record['TRID_INDEX_TERMS'] = [term.text for term in xml_record.xpath("./index_terms/*")]
      record['TRID_SUBJECT_AREAS'] = [subject.text for subject in xml_record.xpath("./subject_areas/*")]

      with open(path.join(JSON_PATH, f'projects/TRID_{xml_record.attrib["id"]}.json'), 'w') as f:
        json.dump(record, f)

      print(f'[project xml2json doc:{xml_record.attrib["id"]}] : Complete')


def publications_xml2json(XML_PATH, JSON_PATH):
  all_xml_files = listdir(XML_PATH)

  def dateCheck(x):
    if x is None:
      return x
    if x[1] > 12 or x[1] < 0:
      x[1] = 1
    if x[2] > 31 or x[2] < 1:
      x[2] = 1
    return x

  for xml_file in all_xml_files:

    file = path.join(XML_PATH, xml_file)

    # parse xml document
    parser = etree.XMLParser(ns_clean=True, remove_blank_text=True, recover=True)
    tree = etree.parse(file,parser)

    # get all project records in the current file
    publication_records_xml = tree.xpath("./record[contains(@type,'component') or contains(@type,'monograph')]")

    record = {}

    for xml_record in publication_records_xml:

      ## get data and store to record dict 

      record['type'] = 'publication'

      # title
      record['title'] = ' '.join(xml_record.findtext("title").split())

      # abstract
      record['abstract'] = ' '.join(xml_record.findtext("abstract") \
        .replace('\n','').split()).replace("\u00ef\u00bf\u00bd",'') # clean up

      # notes
      notes = xml_record.findtext('supplemental_notes')
      record['notes'] = notes.replace('\n','').replace('  ',' ') if notes else None # clean up
    
      # urls
      record['urls'] = []
      record['urls'] = [url.text for url in xml_record.xpath("./document_urls/*")]
      # all_urls = [url.text for url in xml_record.xpath("./document_urls/*")]
      # [record['urls'].append({'url':u}) for u in all_urls]

      # authors
      record['authors'] = []
      for author in xml_record.xpath("./document/authors/*"):
        authors = {}
        authors['firstname'] = author.attrib.get('firstname',None)
        authors['lastname'] = author.attrib.get('lastname',None)
        authors['position'] = author.attrib.get('position',None)
        record['authors'].append(authors)

      # serial
      serial = xml_record.xpath("./document/monograph/serial")
      record['serial'] = serial[0].text if serial else None

      # serial_url
      serial_url = xml_record.xpath("./document/monograph/serial")
      record['serial_url'] = serial_url[0].attrib.get('serialurl', None) if serial_url else None

      # publisher
      publisher = xml_record.xpath("./document/monograph/serial")
      record['publisher'] = publisher[0].attrib.get('publisher',None) if publisher else None

      # publication date
      pub_date = xml_record.xpath("./document/monograph/publication_date")
      pub_date = [int(pub_date[0].attrib.get(x, '01')) for x in ('year','month','day')] if pub_date else None
      pub_date = dateCheck(pub_date)
      pub_date = datetime(pub_date[0], pub_date[1], pub_date[2]).isoformat()[0:10] if pub_date else None
      record['publication_date'] = pub_date

      # tags
      record['tags'] = []

      # TRID meta data 
      record['TRID_RECORD_BASE'] = xml_record.base
      record['TRID_RECORD_ID'] = xml_record.attrib['id']
      record['TRID_RECORD_TYPE'] = xml_record.attrib['type']
      record['TRID_TRIS_FILE_CODES'] = [code.text for code in xml_record.xpath("./tris_files/*")]
      record['TRID_INDEX_TERMS'] = [term.text for term in xml_record.xpath("./index_terms/*")]
      record['TRID_SUBJECT_AREAS'] = [subject.text for subject in xml_record.xpath("./subject_areas/*")]

      with open(path.join(JSON_PATH, f'publications/TRID_{xml_record.attrib["id"]}.json'), 'w') as f:
        json.dump(record, f)

      print(f'[publication xml2json doc:{xml_record.attrib["id"]}] : Complete')
