# TODO: save transformed files as XML, CSV, and json with utf-8 encoding

from datetime import datetime
from lxml import etree

file = './files/TRIDXML_2018-05-13.xml'

# parse xml document
parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
tree = etree.parse(file,parser)

# get all project records in the current file
project_records = tree.xpath("./record[@type='project']")


for record in project_records:

  root = etree.Element('record')

  # record id
  id = etree.Element('id')
  id.text = record.attrib['id']
  root.append(id)

  # record title
  title = etree.Element('title')
  title.text = record.findtext("title")
  root.append(title)

  # abstract
  abstract = etree.Element('abstract')
  text = record.findtext(
    "abstract").replace('\n','').replace('  ',' ') # clean up
  abstract.text = text
  root.append(abstract)

  # notes
  notes = etree.Element('notes')
  text = record.findtext('supplemental_notes')
  if text:
    text = text.replace('\n','').replace('  ',' ') # clean up
  else:
    text = ''
  notes.text = text
  root.append(notes)

  # urls
  url_list = []
  for url in record.xpath("./document_urls/*"):
    url_list.append(url.text)
  urls = etree.Element('urls')
  urls.text = ', '.join(url_list)
  root.append(urls)

  # project status
  project_status = etree.Element('project_status')
  project_status.text = record.xpath("./project/project_status")[0].text
  root.append(project_status)

  # project funding
  project_funding = etree.Element('project_funding')
  project_funding.text = record.xpath("./project/funding")[0].text
  root.append(project_funding)

  # project start date
  project_start = etree.Element('project_start')
  date = record.xpath("./project/start_date")[0].text
  if (date == '0') or (date is None):
    project_start.text = ''
  else:
    d = datetime.strptime(date,'%Y%m%d')
    project_start.text = d.isoformat()[0:10]
  root.append(project_start)

  # project expected completion date
  project_expected_complete = etree.Element('project_expected_complete')
  date = record.xpath("./project/expected_completion_date")[0].text
  if (date == '0') or (date is None):
    project_expected_complete.text = ''
  else:
    d = datetime.strptime(date,'%Y%m%d')
    project_expected_complete.text = d.isoformat()[0:10]
  root.append(project_expected_complete)

  # project actual completion date
  project_actual_complete = etree.Element('project_actual_complete')
  date = record.xpath("./project/actual_completion_date")[0].text
  if (date == '0') or (date is None):
    project_actual_complete.text = ''
  else:
    d = datetime.strptime(date,'%Y%m%d')
    project_actual_complete.text = d.isoformat()[0:10]
  root.append(project_actual_complete)

  # project performing agencies
  agency_list = []
  for agency in record.xpath("./project/performing_agencies/*"):
    agency_list.append(agency.text)
  project_performing_agencies = etree.Element('project_performing_agencies')
  project_performing_agencies.text = ', '.join(agency_list)
  root.append(project_performing_agencies)
  
  # project funding agencies
  funding_list = []
  for funding_agency in record.xpath("./project/funding_agencies/*"):
    funding_list.append(funding_agency.text)
  project_funding_agencies = etree.Element('project_funding_agencies')
  project_funding_agencies.text = ', '.join(funding_list)
  root.append(project_funding_agencies)

  # project investigators
  investigator_list = []
  for investigator in record.xpath("./project/project_investigators/*"):
    investigator_list.append(investigator.text)
  project_investigators = etree.Element('project_investigators')
  project_investigators.text = ', '.join(investigator_list)
  root.append(project_investigators)

  # project responsible individuals
  resp_list = []
  for resp_ind in record.xpath("./project/responsible_individuals/*"):
    resp_list.append(resp_ind.text)
  project_responsible_individuals = etree.Element('project_responsible_individuals')
  project_responsible_individuals.text = ', '.join(resp_list)
  root.append(project_responsible_individuals)

  # TRID RECORD BASE
  base = etree.Element('TRID_RECORD_BASE')
  base.text = record.base
  root.append(base)

  # TRID RECORD ID
  id = etree.Element('TRID_RECORD_ID')
  id.text = record.attrib['id']
  root.append(id)

  # TRID RECORD TYPE
  record_type = etree.Element('TRID_RECORD_type')
  record_type.text = 'project'
  root.append(record_type)

  # TRID TRIS FILE CODES
  code_list = []
  for code in record.xpath("./tris_files/*"):
    code_list.append(code.text)
  codes = etree.Element('TRID_TRIS_FILE_CODES')
  codes.text = ', '.join(code_list)
  root.append(codes)

  # TRID INDEX TERMS
  term_list = []
  for term in record.xpath("./index_terms/*"):
    term_list.append(term.text)
  terms = etree.Element('TRID_INDEX_TERMS')
  terms.text = ', '.join(term_list)
  root.append(terms)

  # TRID SUBJECT AREAS
  subject_list = []
  for subject in record.xpath("./subject_areas/*"):
    subject_list.append(subject.text)
  subjects = etree.Element('TRID_SUBJECT_AREAS')
  subjects.text = ', '.join(subject_list)
  root.append(subjects)

  # TRID PROJECT RIP RECORD
  # 

  with open(f'./files/transformed/{record.attrib["id"]}.xml', 'wb') as xml:
    xml.write(etree.tostring(root, 
      pretty_print = True, xml_declaration=True, encoding='UTF-8'))




