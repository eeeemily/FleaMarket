import os
from flask import Flask, render_template, session, redirect, url_for, flash 
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
application=app
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

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
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    register = SubmitField('Register')

class AddProductForm(FlaskForm):
    product_title = StringField ('Product Name', validators=[DataRequired()])
    product_description = StringField ('Product Description', validators=[DataRequired()])
    price = DecimalField ('Product Price', validators=[NumberRange(min=0)])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Add Product')


# database construction: https://www.youtube.com/watch?v=juPQ04_twtA

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    products = db.relationship('Product', backref='author')

    def __repr__(self):
        return '<Name %r>' % self.id

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

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

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    product_form = AddProductForm()
    if product_form.validate_on_submit():
        photo = product_form.photo.data
        filename = photo.filename
        photo.save(os.path.join(app.instance_path, 'photos', filename))

        title = product_form.product_title.data
        description = product_form.product_description.data
        photo_path = os.path.join(app.instance_path, 'photos', filename)
        
        product = Product(title=title, description=description, photo_path=photo_path)
        print("product created", title, description, photo_path)
        db.session.add(product)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add_product.html', product_form=product_form)

        
