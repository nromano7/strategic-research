from flask import render_template, request, session, url_for
from flaskapp import application
from elastic import query
from dashapp.dashapp import app as dashapp
import json

@application.route("/", methods=['GET', 'POST'])
def home():

  # get request args
  # page = request.args.get('page', 1, type=int)

  # get and handle form data
  # TODO: screen form inputs
  doc_type = request.form.get('recordType','projects')
  sort_by = request.form.get('sortBy','_score')
  # rpp = request.form.get('rpp','5')

  filters=dict(
    element = request.form.get('element','untreated_deck'),
    status = request.form.get('status','active'),
    date_range = request.form.get('dateRange','1'),
    sort_by=sort_by,
    doc_type=doc_type,
    # rpp=rpp
  )
  
  categories = ['construction_quality','design_and_details','material_specifications',
    'live_load', 'environment', 'maintenance_and_preservation',
    'structural_integrity', 'structural_condition', 'functionality', 'cost'
  ]

  content=dict()
  for category in categories:

    # specify index
    index = doc_type
    if index == 'all':
      index = ['projects','publications']

    # run query
    q = query.get_topic_query(category, filters=filters, index=index)
    s = query.run_query(index, q, filters=filters)

    # pagination
    # s = s[(page - 1)*int(rpp):page*int(rpp)]

    # execute and store in content strucutre
    r = s.execute()
    content[category] = r

  return render_template('explore.html',content=content, buttonStates=filters, heading='Strategic Research Matrices')

@application.route("/analysis")
def analysis():
  # return "Analysis"
  return render_template('analyze.html', title='Analysis', heading='Analyze')
