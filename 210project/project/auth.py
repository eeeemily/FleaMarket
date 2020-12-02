

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length 
from . import db

auth = Blueprint('auth', __name__)

class AddProductForm(FlaskForm):
    product_title = StringField ('Product Name', validators=[DataRequired()])
    product_description = StringField ('Product Description', validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Add Product')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    login = SubmitField('Submit')

class RegisterForm(FlaskForm):
    name= StringField ('Full Name', validators=[DataRequired()])
    email = StringField ('Email', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match'), Length(min=6, max=15, message="Password must be at least 6 characters")])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired()])
    register = SubmitField('Register')

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    remember = True if form.remember.data else False

    user = User.query.filter_by(email=email).first()

  
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    form = RegisterForm()
    return render_template('signup.html', form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
    form = RegisterForm()
    email = form.email.data
    password = form.new_password.data
    name = form.name.data
    

    user = User.query.filter_by(email=email).first() 
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

  
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))