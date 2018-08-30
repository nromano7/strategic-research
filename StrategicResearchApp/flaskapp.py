from flask import Flask, render_template, url_for
app = Flask(__name__)


documents = [
  {
    "doc_type":"project",
    "title":"Some Project Title",
    "abstract":"This is a summary of the project."
  },
  {
    "doc_type":"publication",
    "title":"Some Publication Title",
    "abstract":"This is a summary of the publication."
  }
]


@app.route("/")
@app.route("/srm")
def home():
  return render_template('home.html', documents=documents)

@app.route("/analysis")
def analysis():
  return render_template('analysis.html')



if __name__ == '__main__':
  app.run(debug=True)