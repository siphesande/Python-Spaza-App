from flask import Flask, render_template, flash, request, url_for, redirect
from wtforms import Form
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
@app.route('/login/', methods = ['GET','POST'])
def login_page():
    
    return render_template("login.html")


@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	session.clear()
	flash('You have been logged out.')
	gc.collect()
	return redirect(url_for('main'))
class RegistratiopnForm(Form):
	username = TextField("Username", [validators.Length(min =4, max =20)])
	email = TextField("Email Address", [validators.Length(min = 6, max= 50)])
	password = PasswordField("Password", [validators.Required(),
		                                  validators.EqualTo("confirm", message = "Passwords Must macth." )])
	confirm = PasswordField("Repeat Password")
	accept_tos = BooleanField("I accept the <a href="/tos/">Terms of Service and the <a href = "/privacy/">Privacy Notice </a> (Last updated Dec 2015)",[validators.Required])


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
	try:
		c, conn = connection()
		return("okay")
	except Exception as e:
		return(str(e))

    

# @app.route("/slashboard")
# def slashboard():
# 	try:
# 	    return render_template("dashboard.html")
#     except Exception as e:
#         return render_template("500.html",error = e)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=12345, use_reloader=True)