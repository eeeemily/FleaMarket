from flask import Flask, render_template, session, redirect, url_for, flash 
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'
application=app
bootstrap = Bootstrap(app)
moment = Moment(app)




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    login = SubmitField('Submit')



class RegisterForm(FlaskForm):
    name= StringField ('Full Name', validators=[DataRequired()])
    email = StringField ('Email', validators=[DataRequired(), Email()])
    new_username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match'), Length(min=6, max=15, message="Password must be at least 6 characters")])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired()])
    register = SubmitField('Register')

class Users(db.Model):
    username =db.Column(db.String(), primary_key=True, unique=True)
    name=db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #date_created=db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Name %r>' % self.id


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index(): 
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
       old_name=session.get('username')
       if old_name is not None and old_name != form.username.data:
           flash('Looks like you have changed your username!')
       session['username'] = form.username.data
       form.username.data=""
       session['password']=form.password.data
       return redirect(url_for('index'))
     
       
       
    return render_template('login.html', form=form, name=session.get('username'), type1= session.get('password'))

@app.route('/logout')
def logout(): 
    return render_template('home.html')

@app.route('/register' , methods=['GET', 'POST'] )
def register(): 
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        session['email'] = register_form.email.data
        session['new_username'] = register_form.new_username.data
        register_form.new_username.data=""
        session['new_password'] = register_form.new_password.data
        register_form.new_password.data=""
        session['confirm_password'] = register_form.confirm_password.data
        register_form.confirm_password.data=""
        return redirect(url_for('index'))

    return render_template('register.html', register_form=register_form)




        
