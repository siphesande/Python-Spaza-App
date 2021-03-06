from flask import Flask, render_template, flash, request, url_for, redirect,session
from wtforms import Form

from wtforms import Form, BooleanField, TextField, PasswordField, validators
from dbconnect import connection
from passlib.hash import sha256_crypt
from functools import wraps
from MySQLdb import escape_string as thwart
import gc
import os


app = Flask(__name__)

@app.route('/')
def homepage():
    
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
	flash("flash test!!!")
	return render_template("dashboard.html")
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route('/login/', methods=['GET','POST'])
def login():
    try:
        c,conn = connection()
        
        error = None
        if request.method == 'POST':

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                    thwart(request.form['username']))
            data = c.fetchone()[2]


            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash('You are now logged in.'+str(session['username']))
                return redirect(url_for('dashboard'))

            else:
                error = 'Invalid credentials. Try again'
        gc.collect()
        return render_template('login.html', error=error)
    except Exception, e:
        error = 'Invalid credentials. Try again'
        return render_template('login.html', error=error)
# @app.route('/login/', methods = ['GET','POST'])
# def login_page():
    
#     return render_template("login.html")


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('You have been logged out.')
	gc.collect()
	return redirect(url_for('homepage'))
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(),
                                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/about/tos" target="blank">Terms of Service</a> and <a href="/about/privacy-policy" target="blank">Privacy Notice</a> (updated Jan 22, 2015)', [validators.Required()])

# class RegistratiopnForm(Form):
# 	username = TextField("Username", [validators.Length(min =4, max =20)])
# 	email = TextField("Email Address", [validators.Length(min = 6, max= 50)])
# 	password = PasswordField("Password", [validators.Required(),
# 		                                  validators.EqualTo("confirm", message = "Passwords Must macth." )])
# 	confirm = PasswordField("Repeat Password")
# 	accept_tos = BooleanField("I accept the <a href='/about/tos/'>Terms of Service and the <a href = '/privacy/'>Privacy Notice </a> (Last updated Dec 2015)",[validators.Required])
@app.route('/register/', methods=['GET', 'POST'])
def register():

    try:
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            flash("register attempted")

            username = form.username.data
            email = form.email.data

            password = sha256_crypt.encrypt((str(form.password.data)))
            c,conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                    (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))
                conn.commit()
                flash('Thanks for registering')
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
        gc.collect()
        flash("hi there.")
        return render_template('register.html', form=form)
    except Exception as e:
        return(str(e))


# @app.route('/register/', methods=['GET', 'POST'])
# def register_page():
# 	try:
# 		form = RegistrationForm(request.form)
# 		if request.method == "POST" and form.validate():
# 			username = form.username.date
# 			email =form.email.data
# 			password = sha256_crypt.encrypt(((str(form.password.date))))
#             c, conn = connection() 

#             x = c.execute("SELECT * FROM users WHERE username = (%s)",
#             	(thwart(username)))
#             if int(x) > 0:
#             	flash("That username is already taken, please choose another")
#             	return render_template('register.html', form-form)

#             else:
#             	c.execute("INSERT INTO users (username,password,email, tracking) VALUES (%s, %s, %s, %s),
#                        (thwart(username),thwart(password),thwart(email),thwart("/introduction-to-python-programming/"))
#                 conn.commit()
#                 flash("Thanks for registering!")
#                 c.close()
#                 conn.close()

#                 gc.collect()

#                 session['logged_in'] = True
#                 session['username'] = username

#                 return redirect(url_for("dashboard"))

# return render_template("register.html", form=form)


# 	except Exception as e:
# 		return(str(e))

    

# @app.route("/slashboard")
# def slashboard():
# 	try:
# 	    return render_template("dashboard.html")
#     except Exception as e:
#         return render_template("500.html",error = e)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True)