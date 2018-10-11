from flask import Flask

application = Flask(__name__)

@application.route("/")
def home():
  return "Home"
  
if __name__ == '__main__':
  application.run(debug=True)
