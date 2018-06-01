# Notes for TRID

## URL Query Keywords <hr>

https://trid.trb.org/Results?...  

	txtKeywords=&... [keyword filter] ***required***  
	txtTitle=&... [title filter]  
	txtSerial=&... [serial or conference filter]  
	ddlSubject=1797&... [subject area filter (*1797=Bridges and structures)] ***required***  
	txtReportNum=&... [paper/report/contract/grant filter]
	ddlTrisfile=&... [source filter] ***required***  
	txtIndex=%20&... [index term filter]  
	specificTerms=&... []  
	txtAgency=&... [organization/agency fitler]   
	txtAuthor=&... [person/author filter]  
	ddlResultType=&... [result type filter]  
	chkFulltextOnly=0&... []  
	language=&... [language filter (1=english)]  
	subjectLogic=or&... []  
	dateStart=&... [start date (e`x. 201305)]  
	dateEnd=&... [end date (ex. 201808)]  
	rangeType=&... [date range type (publisheddate or *recordcreateddate)]  
	sortBy=&... [sort by]  
	sortOrder=DESC&... [sort order]  
	rpp=25 [results per page (10,25,50,100)]  

## Data Extraction  <hr>

Procedure:`

	1) search

	2) "click" to mark 'Page' or 'All'

		- document.getElementById("mark-page").click()

	3) "click" the 'Save' link
	
		- $('#save_modal').modal('show')

	4) select "XML" radio button
	
		- document.querySelectorAll("input[value=XML]")[1].click()

	5) "click" the 'Download' button
	
		- document.getElementById("saveMarkedResults").click()

	6) click 'clear' to deselect all
	
		- document.getElementById("mark-clear").click()

	7) click to go to next page

		- document.getElementsByClassName("record-pagination-forward")[0].click()

	8) repeat from 2

## XML Files <hr>

- All records are either a 'project' or 'document' (monograph/component)
- Project records have a project element containing certain project informtion
- Document records have a document element containing document information
- Some fields have related information that we may wish to save (e.g. performing agencies have address or url) 

### Potential Fields for SRM Database <hr>

- CAPS indicate fields for TRID meta data
- saving TRID meta data in case we need to refer back to where the record came from

#### Fields present for all records:
	record_id = ?

		- INT or CHAR
		- unique identifier of the record
		- auto-increment or some hash code

	record_type = ?

		- CHAR
		- identifies the record as a project or document
		- record(type) = project (for projects), monograph/component (for documents)
		- record.record_type = PR (for project), DO (for document)

	record_title = record.title

		- VARCHAR
		- title of project or document

	record_abstract = record.abstract

		- TEXT
		- abstract describing project or document

	record_notes = record.supplemental_notes

		- TEXT
		- some records have supplemental notes

	record_urls = [record.document_urls.url]

		- VARCHAR
		- a list of one or many urls
		- urls have @type = D (for "Record URL"), and S (for "Summary URL")

	TRID_RECORD_BASE = record.base

		- VARCHAR
		- the base is the raw xml file the record was taken from

	TRID_RECORD_ID = record(id)

		- INT
		- save id from TRID database just in case we need to reference it later

	TRID_RECORD_TYPE = ?

		- VARCHAR
		- this may or may not be the same as 'record_type' so it may not be needed
		- record(type) = project (for projects), monograph/component(for documents)
		- record.record_type = PR (for project), DO (for document)

	TRID_TRIS_FILE_CODES = [record.tris_files.tris_file]

		- TEXT
		- a list of one or many file codes
		- these seem to indicate where the record is coming from 
		- codes = {USDOT, ASCE, NTL, ATRI, TLI, TRIS, STATEDOT, UTC, RiP, TRB}

	TRID_INDEX_TERMS = [record.index_terms.term]

		- TEXT
		- a list of one or many index terms
		- terms have @type = IT (for TRT term), UT (for "uncontrolled terms"), PT (?), GT (Geographic term?)

	TRID_SUBJECT_AREAS = [record.subject_areas.subject_area]

		- TEXT
		- a list of one or many subject areas
		- subject areas identify a record by specific transportation mode, function, or activity

#### Fields present for 'project' records:

	project_status = record.project.project_status

		- VARCHAR or CHAR
		- attributes: completed (@code=CO), active (@code=AP), proposed (@code=PR), programmed (@code=PG)

	project_funding = record.project.funding

		- INT
		- funding for project in dollar amount
		- not always available

	project_start = record.project.start_date

		- DATE
		- project start date mostly available

	project_expected_complete = record.project.expected_completion_date

		- DATE
		- expected completion date not always available (0 if None)

	project_actual_complete = record.project.actual_completion_date

		- DATE
		- actual completion date not always available (0 if None)

	project_performing_agency = [record.project.performing_agencies.performing_agency]

		- TEXT
		- a list of one or more performing agencies
		- attributes: street, city, region, country, and url to performing agency

	project_funding_agency = [record.project.funding_agencies.funding_agency]

		- TEXT
		- a list of one or more funding agencies
		- attributes: street, city, region, country, and url to funding agency

	project_investigator = [record.project.investigators.investigator]

		- VARCHAR or TEXT
		- a list of one or more project investigators
		- attributes: firstname, lastname

	project_responsible_individual = [record.project.responsible_individuals.responsible_individual]

		- VARCHAR or TEXT
		- a list of one or more responsible individuals
		- attributes: firstname, lastname
		- not sure the difference between this and project investigator
	
	TRID_PROJECT_RIP_RECORD = record.project.rip_record

		- VARCHAR
		- save project RiP record identifier just in case its needed later

#### Fields present for 'document' (component/monograph) records 

	document_author = [record.document.authors.author]

		- VARCHAR or TEXT
		- a list of one or more authors
		- attributes: firstname, lastname, *position

	document_serial = record.document.monograph.serial

		- VARCHAR
		- document serial (i.e. publication)
		- attributes: publisher, serialurl

	document_publication_date = record.document.monograph.publication_date

		- DATE
		- attributes: year, month

#### TBD fields 

	source_agency

		- examples: Federal Highway Administration, Nevada DOT, Northwestern University Transportation Library
		- only present in 25/100 records
		- appears to always be present for project records
		- attributes: street, city, region, country, and site_url  

	source_data

		- rarely available, and not sure what data it holds

	contract_numbers
		
		- some projects and monographs have contract numbers

	project_deliverables
	
		- record.project has deliverables field but it's empty

	project_manager_agency
	
		- may be same as performing agency
		- attributes: street, city, region, country, and site_url 

	report_numbers
	
		- seems like only monographs have them

	record.document.media_type

	record.document.features

	record.document.monograph.corprate_authors






