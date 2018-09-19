from flask import render_template, request, url_for
from flaskapp import app
from elastic.models import Project, Publication
from elastic import client, query
from dashapp.dashapp import app as dashapp
import json

@app.route("/", methods=['GET', 'POST'])
# @app.route("/srm", methods=['GET', 'POST'])
def home():

  # get request args
  page = request.args.get('page', 1, type=int)
  

  # get form data
  doc_type = request.form.get('recordType','projects')
  sort_by = request.form.get('sortBy','_score')
  filters=dict(
    record_set = request.form.get('recordSet','all'),
    status = request.form.get('status','all'),
    date_range = request.form.get('dateRange','10'),
    tags = request.form.get('tags','all')
  )
  # rpp = int(request.form.get('rpp',5))
   # TODO: screen form inputs

  # handle form data
  index = doc_type
  if index == 'all':
    index = ['projects','publications']


  content=dict()
  categories = ['construction_quality','design_and_details','material_specifications',
    'live_load', 'environment', 'maintenance_and_preservation',
    'structural_integrity', 'structural_condition', 'functionality', 'cost'
  ]

  for category in categories:

    q = query.get_query(category, filters, index)
    # print(json.dumps(q,indent=2))
    s = query.run_query(index, q)
    if sort_by == 'date':
      if index == 'projects':
        s.sort("-expected_complete_date","-actual_complete_date",'-start_date')
      elif index == 'publications':
        s.sort("-publication_date")
    # s = Project.search(using=client, index='projects').query(q)[:rpp]#[:((page - 1) * rpp + 1)]
    r = s.execute()
    content[category] = r

  return render_template('home.html',content=content, buttonStates=filters, heading='Strategic Research Matrices')

@app.route("/analysis")
def analysis():
  return render_template('analysis.html', title='Analysis', heading='Analysis')
  # return dashapp.index()


# @app.route("/test", methods=['GET', 'POST'])
# def test():
#   return f"{request.form['rpp']}"