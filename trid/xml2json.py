from datetime import datetime
import json
from lxml import etree
from os import listdir, path

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

def dateCheck_pub(x):
  if x is None:
    return x
  if x[1] > 12 or x[1] < 0:
    x[1] = 1
  if x[2] > 31 or x[2] < 1:
    x[2] = 1
  return x

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

def xml2json(XML_PATH, JSON_PATH):

  # get list of all xml files in XML_PATH
  all_xml = listdir(XML_PATH)

  for file in all_xml:

    # path to xml file
    xml_path = path.join(XML_PATH, file)

    # parse xml document
    parser = etree.XMLParser(ns_clean=True, remove_blank_text=True, recover=True)
    tree = etree.parse(xml_path, parser)

    # parse xml and store records in dict
    
    all_records = tree.xpath("./record")

    for rec in all_records:
      record = {}

      # TRID meta data 
      record['TRID_RECORD_BASE'] = rec.base
      record['TRID_RECORD_ID'] = rec.attrib['id']
      record['TRID_RECORD_TYPE'] = rec.attrib['type'] 
      record['TRID_TRIS_FILE_CODES'] = [code.text for code in rec.xpath("./tris_files/*")]
      record['TRID_INDEX_TERMS'] = [term.text for term in rec.xpath("./index_terms/*")]
      record['TRID_SUBJECT_AREAS'] = [subject.text for subject in rec.xpath("./subject_areas/*")]
     
      # tags
      record['tags'] = []

      # title
      record['title'] = ' '.join(rec.findtext("title").split())

      # abstract
      try:
        record['abstract'] = ' '.join(rec.findtext("abstract") \
          .replace('\n','').split()).replace("\u00ef\u00bf\u00bd",'') # clean up
      except:
        print()

      # notes
      notes = rec.findtext('supplemental_notes')
      record['notes'] = notes.replace('\n','').replace('  ',' ') if notes else None # clean up
    
      # urls
      record['urls'] = []
      record['urls'] = [url.text for url in rec.xpath("./document_urls/*")]

      if rec.attrib['type'] == "project":

        # project status
        try:
          record['status'] = rec.xpath("./project/project_status")[0].text
        except:
          print()

        # project funding
        try:
          funding = rec.xpath("./project/funding")[0].text
          record['funding'] = None if funding is None else fundingCheck(funding.replace(',','').split('$')[-1])
        except:
          print()

        # project start date
        start_date = rec.xpath("./project/start_date")[0].text
        record['start_date'] = None if start_date is '0' else dateCheck(start_date)

        # project expected completion date
        expected_complete = rec.xpath("./project/expected_completion_date")[0].text
        record['expected_complete_date'] = None if expected_complete is '0' else dateCheck(expected_complete)

        # project actual completion date
        actual_complete = rec.xpath("./project/actual_completion_date")[0].text
        record['actual_complete_date'] = None if actual_complete is '0' else dateCheck(actual_complete)

        # project performing agencies
        record['performing_agencies'] = []
        for perf_agency in rec.xpath("./project/performing_agencies/*"):
          agency = agencyCheck(perf_agency)
          if agency['state'] == "United States" or agency['state'] == "USA":
            agency['state'] = fixStateName(agency.get('state'))
          record['performing_agencies'].append(agency)

        # project funding agencies
        funding_agencies = rec.xpath("./project/funding_agencies/*")
        record['funding_agencies'] = []
        for fund_agency in funding_agencies:
          agency = agencyCheck(fund_agency)
          if agency['state'] == "United States" or agency['state'] == "USA":
            agency['state'] = fixStateName(agency.get('state'))
          record['funding_agencies'].append(agency)

        # project managing agencies
        record['managing_agencies'] = []
        for manage_agency in rec.xpath("./project/manager_agencies/*"):
          agency = agencyCheck(manage_agency)
          if agency['state'] == "United States" or agency['state'] == "USA":
            agency['state'] = fixStateName(agency.get('state'))
          record['managing_agencies'].append(agency)

        # project investigators
        record['project_investigators'] = []
        for investigator in rec.xpath("./project/investigators/*"):
          individual = {}
          individual['firstname'] = investigator.attrib['firstname']
          individual['lastname'] = investigator.attrib['lastname']
          record['project_investigators'].append(individual)

        # project responsible individuals
        record['responsible_individuals'] = []
        for resp_individual in rec.xpath("./project/responsible_individuals/*"):
          individual = {}
          individual['firstname'] = resp_individual.attrib['firstname']
          individual['lastname'] = resp_individual.attrib['lastname']
          record['responsible_individuals'].append(individual)

        with open(path.join(JSON_PATH, f'projects/TRID_{rec.attrib["id"]}.json'), 'w') as f:
          json.dump(record, f)

        print(f'[project xml2json doc:{rec.attrib["id"]}] : Complete')

      else:

        # publication authors
        record['authors'] = []
        for author in rec.xpath("./document/authors/*"):
          authors = {}
          authors['firstname'] = author.attrib.get('firstname',None)
          authors['lastname'] = author.attrib.get('lastname',None)
          authors['position'] = author.attrib.get('position',None)
          record['authors'].append(authors)

        # publication serial
        serial = rec.xpath("./document/monograph/serial")
        record['serial'] = serial[0].text if serial else None

        # publication serial_url
        serial_url = rec.xpath("./document/monograph/serial")
        record['serial_url'] = serial_url[0].attrib.get('serialurl', None) if serial_url else None

        # publisher
        publisher = rec.xpath("./document/monograph/serial")
        record['publisher'] = publisher[0].attrib.get('publisher',None) if publisher else None

        # publication date
        pub_date = rec.xpath("./document/monograph/publication_date")
        pub_date = [int(pub_date[0].attrib.get(x, '01')) for x in ('year','month','day')] if pub_date else None
        pub_date = dateCheck_pub(pub_date)
        pub_date = datetime(pub_date[0], pub_date[1], pub_date[2]).isoformat()[0:10] if pub_date else None
        record['publication_date'] = pub_date

        with open(path.join(JSON_PATH, f'publications/TRID_{rec.attrib["id"]}.json'), 'w') as f:
          json.dump(record, f)

        print(f'[publication xml2json doc:{rec.attrib["id"]}] : Complete')


XML_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\xml\publications"
JSON_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json"

xml2json(XML_PATH, JSON_PATH)