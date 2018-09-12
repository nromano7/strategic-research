from flask import render_template, url_for
from flaskapp import app, client
from elastic.models import Project, Publication
from elastic import query

@app.route("/")
@app.route("/srm")
def home():
  content=dict()
  categories = ['construction_quality','design_and_details','material_specifications',
    'live_load', 'environment', 'maintenance_and_preservation',
    'structural_integrity', 'structural_condition', 'functionality', 'cost'
  ]
  for category in categories:
    q = query.get_query(category)
    s = Project.search(using=client, index='projects').query(q)[:3]
    response = s.execute()
    content[category] = response
  return render_template('home.html',content=content, heading='Strategic Research Matrices')

@app.route("/analysis")
def analysis():
  return render_template('analysis.html', title='Analysis', heading='Analysis')