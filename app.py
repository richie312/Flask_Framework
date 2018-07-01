from flask import Flask, render_template, flash, redirect,url_for,session, logging,request
from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt



Articles=Articles()

app=Flask(__name__)


## Config MySql

app.config ["MYSQL_HOST"] = 'localhost'
app.config ["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'myflaskapp'
app.config ['MYSQL_CURSORCLASS'] = 'DictCursor'

## Initialise the sql instance

mysql = MySQL(app)


@app.route('/')

def index():
	return render_template("home.html")

@app.route('/Boston') 
def Boston():
    return render_template('boston.html')

@app.route('/Stock') 
def Stock():
    return render_template('Stock.html')

@app.route('/articles') 
def articles():
    return render_template('Articles.html', articles = Articles)

@app.route('/article/<string:id>/') 
def article(id):
    return render_template('article.html', id = id)

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1,max=50)])
	username = StringField('username',[validators.Length(min=4,max=25)])
	email = StringField('email',[validators.Length(min=6,max=50)])
	password=PasswordField('password',[validators.DataRequired(),
		validators.EqualTo('confirm', message="passwords do not match")
		])
	confirm = PasswordField("confirm Password")

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username=form.username.data
		password=sha256_crypt.encrypt(str(form.password.data))

		## Create the cursor
		cur= mysql.connection.cursor()
		cur.execute("INSERT INTO users(name,email,username,password VALUES(%s, %s, %s, %s)",
			(name,email,username,password))
		## Commit to db
		mysql.connection.commit()

		## Close Connection

		cur.close()

		flash("You are now registered and can login in", "Success")
		return(url_for("index"))

	return render_template('register.html',form=form)


if __name__=='__main__':
	app.run(debug=True)