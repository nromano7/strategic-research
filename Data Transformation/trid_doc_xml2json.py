from datetime import datetime
import json
from lxml import etree
from os import listdir, path

# TODO: write to xml and csv

RAW_FILES_PATH =r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\raw"
TRANS_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\publications"
all_xml_files = listdir(RAW_FILES_PATH)

def dateCheck(x):
  if x is None:
    return x
  if x[1] > 12 or x[1] < 0:
    x[1] = 1
  if x[2] > 31 or x[2] < 1:
    x[2] = 1
  return x

for xml_file in all_xml_files:

  file = path.join(RAW_FILES_PATH, xml_file)

  # parse xml document
  parser = etree.XMLParser(ns_clean=True, remove_blank_text=True, recover=True)
  tree = etree.parse(file,parser)

  # get all project records in the current file
  publication_records_xml = tree.xpath("./record[contains(@type,'component') or contains(@type,'monograph')]")

  record = {}

  for xml_record in publication_records_xml:

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

    # authors
    record['authors'] = []
    for author in xml_record.xpath("./document/authors/*"):
      authors = {}
      authors['first_name'] = author.attrib.get('firstname',None)
      authors['last_name'] = author.attrib.get('lastname',None)
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

    # TRID meta data 
    record['TRID_RECORD_BASE'] = xml_record.base
    record['TRID_RECORD_ID'] = xml_record.attrib['id']
    record['TRID_RECORD_TYPE'] = xml_record.attrib['type']
    record['TRID_TRIS_FILE_CODES'] = [code.text for code in xml_record.xpath("./tris_files/*")]
    record['TRID_INDEX_TERMS'] = [term.text for term in xml_record.xpath("./index_terms/*")]
    record['TRID_SUBJECT_AREAS'] = [subject.text for subject in xml_record.xpath("./subject_areas/*")]

    with open(path.join(TRANS_FILES_PATH, f'TRID_{xml_record.attrib["id"]}.json'), 'w') as f:
      json.dump(record, f)


