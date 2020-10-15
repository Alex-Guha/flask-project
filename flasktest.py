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
@app.route('/static/<path>')
def send_css(path):
	return send_from_directory('static', path)

#Handles the form input from the stories page and puts it in feedback.txt
@app.route('/feedback/', methods=['POST', 'GET'])
def feedback():
	if request.method == 'POST':
		first, last, email, feedback = request.form['firstname'], request.form['lastname'], request.form['email'], request.form['feedback']
		with open('templates/feedback.txt', 'a') as file:
			file.write(first + '\n' + last + '\n' + email + '\n' + feedback + '\r\n')
		return render_template('form_success.html')
	else:
		return render_template('feedback.html')

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/blog/')
def blog():
	return render_template('blog.html')

@app.errorhandler(404)
def notfound(e):
	return render_template('404.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		session.permanent = True
		__user = request.form['user']
		__password = request.form['pass']
		session['user'] = __user
		session['pass'] = __password
		return redirect(url_for('admin'))
	else:
		return render_template('login.html')

@app.route('/admin/')
def admin():
	if 'user' in session:
		__user = session['user']
		__pswrd = session['pass']
		#auth check
		__authorized = False
		__permissions = 'user'
		with open('admin.txt', 'r') as __auth_file:
			for item in __auth_file.readlines():
				__auth_user = eval(item)
				if __auth_user[0] == __user and __auth_user[1] == __pswrd:
					__authorized = True
					__permissions = __auth_user[2]
		if __authorized:
			__admin_list = []
			with open('admin.txt', 'r') as file:
				__admin_list = map(eval, file.readlines())
			return render_template('admin.html', admin_list=__admin_list, user=__user, permissions=__permissions)
		else:
			flash('You don\'t have permission to access the admin page.', 'info')
			return redirect(url_for('login'))
	else:
		flash('You don\'t have permission to access the admin page.', 'info')
		return redirect(url_for('login'))

@app.route('/logout/')
def logout():
	if 'user' in session:
		session.pop('user', None)
		session.pop('pass', None)
		flash('You have been logged out.', 'info')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)

# TODO
# add encryption and access to files