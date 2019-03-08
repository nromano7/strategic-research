from flaskapp import application
import os

if __name__ == '__main__':
	
	if os.environ.get('FLASKHOST'):
		application.run(debug=True, host=os.environ['FLASKHOST'])
	else:
		application.run(debug=True)