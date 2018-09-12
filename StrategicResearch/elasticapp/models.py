from elasticsearch_dsl import (
  Document, 
  Date, 
  Nested, 
  InnerDoc, 
  Keyword, 
  Text, 
  Float, 
  Integer, 
  analyzer, 
  tokenizer, 
  analysis
)

# define custom token filters and anlyzers
bigram_token_filter = analysis.token_filter('bigram', 'shingle', min_shingle_size=2, max_shingle_size=2, output_unigrams=False)
trigram_token_filter = analysis.token_filter('trigram', 'shingle', min_shingle_size=3, max_shingle_size=3, output_unigrams=False)
quadragram_token_filter = analysis.token_filter('quadragram', 'shingle', min_shingle_size=4, max_shingle_size=4, output_unigrams=False)
pentagram_token_filter = analysis.token_filter('pentagram', 'shingle', min_shingle_size=5, max_shingle_size=5, output_unigrams=False)
stemmer_token_filter = analysis.token_filter('english_stemmer', 'stemmer', name="english")

standard = analyzer('standard_analyzer',
  type="custom",
  tokenizer="standard",
  filter=["standard", "lowercase", "stop", stemmer_token_filter],
)
bigram = analyzer('bigram_analyzer',
  type="custom",
  tokenizer="standard",
  filter=[bigram_token_filter, "lowercase", "stop", stemmer_token_filter]
)
trigram = analyzer('trigram_analyzer',
  type="custom",
  tokenizer="standard",
  filter=[trigram_token_filter, "lowercase", "stop", stemmer_token_filter]
)
quadragram = analyzer('quadragram_analyzer',
  type="custom",
  tokenizer="standard",
  filter=[quadragram_token_filter, "lowercase", "stop", stemmer_token_filter]
)
pentagram = analyzer('pentagram_analyzer',
  type="custom",
  tokenizer="standard",
  filter=[pentagram_token_filter, "lowercase", "stop", stemmer_token_filter]
)

# create model classes for document objects
class Agency(InnerDoc):
    name = Text(fields={'keyword': Keyword()})
    city = Text(fields={'keyword': Keyword()})
    state = Text(fields={'keyword': Keyword()})
    country = Text(fields={'keyword': Keyword()})
    postal_code = Text(fields={'keyword': Keyword()})
    site_url = Text(fields={'keyword': Keyword()})

class Person(InnerDoc):
    firstname = Text(fields={'keyword': Keyword()})
    lastname = Text(fields={'keyword': Keyword()})

class Author(Person):
    position = Integer()

class Record(Document):
    TRID_INDEX_TERMS = Text(multi=True, fields={'keyword': Keyword(multi=True)})
    TRID_RECORD_BASE = Text(fields={'keyword': Keyword()})
    TRID_RECORD_ID = Text(fields={'keyword': Keyword()})
    TRID_RECORD_TYPE = Text(fields={'keyword': Keyword()})
    TRID_SUBJECT_AREAS = Text(multi=True, fields={'keyword': Keyword(multi=True)})
    TRID_TRIS_FILE_CODES = Text(multi=True, fields={'keyword': Keyword(multi=True)})
    doc_type = Text(fields={'keyword': Keyword()})
    abstract = Text(fields={'keyword': Keyword(), 
        'bigram': Text(analyzer=bigram), 
        'trigram': Text(analyzer=trigram),
        'quadragram': Text(analyzer=quadragram),
        'pentagram': Text(analyzer=pentagram)}, analyzer=standard)
    notes = Text(fields={'keyword': Keyword(), 
        'bigram': Text(analyzer=bigram), 
        'trigram': Text(analyzer=trigram),
        'quadragram': Text(analyzer=quadragram),
        'pentagram': Text(analyzer=pentagram)}, analyzer=standard)
    title = Text(fields={'keyword': Keyword(), 
        'bigram': Text(analyzer=bigram), 
        'trigram': Text(analyzer=trigram),
        'quadragram': Text(analyzer=quadragram),
        'pentagram': Text(analyzer=pentagram)}, analyzer=standard)
    tags = Text(multi=True, fields={'keyword': Keyword(multi=True), 'bigram': Text(multi=True, analyzer=bigram), 'trigram': Text(multi=True, analyzer=trigram)})
    urls = Text(multi=True)

class Project(Record):
    actual_complete_date = Date(format='yyyy-MM-dd')
    expected_complete_date = Date(format='yyyy-MM-dd')
    funding = Float()
    funding_agencies = Nested(Agency)
    managing_agencies = Nested(Agency)
    performing_agencies = Nested(Agency)
    project_investigators = Nested(Person)
    responsible_individuals = Nested(Person)
    start_date = Date(format='yyyy-MM-dd')
    status = Text(fields={'keyword': Keyword()})

    class Meta:
        index = 'projects'

class Publication(Record):
    authors = Nested(Author)
    publication_date = Date(format='yyyy-MM-dd')
    publisher = Text(fields={'keyword': Keyword()})
    serial = Text(fields={'keyword': Keyword()})

    class Meta:
        index = 'publications'
