#run in cmd with 'python "flask.py"'

from flask import Flask, flash, session, redirect, url_for, render_template, send_from_directory, request
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'changeme'
app.permanent_session_lifetime = timedelta(days=1)

#this decorator designates the route the user searching our webpage takes, in this case, base route.
@app.route('/')
@app.route('/index/')
def home():
	return render_template('index.html')

# Sends the css files, or any file requested (so be careful!)
@app.route('/css/<path>')
def send_css(path):
	return send_from_directory('css', path)

#Handles the form input from the stories page and puts it in feedback.txt
@app.route('/stories/', methods=['POST', 'GET'])
def stories():
	if request.method == 'POST':
		first, last, email, feedback = request.form['firstname'], request.form['lastname'], request.form['email'], request.form['feedback']
		with open('templates/feedback.txt', 'a') as file:
			file.write(first + '\n' + last + '\n' + email + '\n' + feedback + '\r\n')
		return render_template('form_success.html')
	else:
		return render_template('stories.html')

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html')

@app.errorhandler(404)
def notfound(e):
	return render_template('404.html')

@app.route('/admin/', methods=['POST', 'GET'])
def admin():
	if request.method == 'POST':
		session.permanent = True
		_user = request.form['user']
		_password = request.form['pass']
		session['user'] = _user
		session['pass'] = _password
		return redirect(url_for('user'))
	else:
		return render_template('admin.html')

@app.route('/user/')
def user():
	if 'user' in session:
		_user = session['user']
		_pswrd = session['pass']
		#auth check
		return render_template('admin_actual.html')
	else:
		return redirect(url_for('admin'))

@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user', None)
		session.pop('pass', None)
		flash('You have been logged out.', 'info')
	return redirect(url_for('admin'))

if __name__ == '__main__':
	app.run(debug=True)