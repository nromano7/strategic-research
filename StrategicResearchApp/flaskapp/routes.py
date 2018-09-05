from flask import render_template, url_for
from flaskapp import app, client
from flaskapp.models import Project, Publication
from elasticapp import queries

@app.route("/")
@app.route("/srm")
def home():
  content=dict()
  tag = 'construction_quality'
  s = Project.search(using=client, index='projects')
  q = queries.get_query(tag)
  s = s.query(q)
  content[tag] = s.execute()
  return render_template('home.html',content=content, heading='Strategic Research Matrices')

@app.route("/analysis")
def analysis():
  return render_template('analysis.html', title='Analysis', heading='Analysis')