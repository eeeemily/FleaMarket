# all together
# init.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap

# main.py
import os

from flask import Blueprint, redirect, request, render_template, url_for, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length
# from project import auth, models

# auth.py
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from wtforms import DecimalField, SelectField
from wtforms.validators import NumberRange

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)
application = app

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


# from .models import User

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    phone = db.Column(db.String(100))
    products = db.relationship('Product', backref='author')


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo_name = db.Column(db.String(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


main = Blueprint('main', __name__)
# UPLOAD_FOLDER = os.path.join(current_app.root_path, 'instance', 'photos')


@main.route('/')
def index():
    return render_template('index.html', products=Product.query.all(), users=User)


@main.route('/test')
def test():
    return render_template('test.html', products=Product.query.all())


@main.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)

    update_form = auth.EditProductForm(
        title=product.title, description=product.description, price=product.price)
    if update_form.validate_on_submit():
        product.title = update_form.title.data
        product.description = update_form.description.data
        product.price = int(update_form.price.data)
        db.session.commit()
        return redirect(url_for('main.profile'))
    else:
        return render_template('update_product.html', product=product, update_form=update_form)


@main.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('main.profile'))
    except:
        return "There was an error deleting from the database"


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    product_form = AddProductForm()
    if product_form.validate_on_submit():
        photo = product_form.photo.data
        filename = photo.filename

        # print("PATH = ", os.path.join(current_app.root_path)
        # download the photo
        photo.save(os.path.join('static',
                                'instance', 'photos', filename))

        title = product_form.title.data
        description = product_form.description.data
        price = product_form.price.data
        price = int(price)
        photo_name = filename

        author_id = User.query.filter_by(name=current_user.name).first().id

        product = Product(title=title, description=description,
                          price=price, photo_name=photo_name, author_id=author_id)

        db.create_all()
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('profile.html', product_form=product_form, name=current_user.name, products=Product.query.filter_by(author_id=current_user.id).all())


# blueprint for non-auth parts of app
app.register_blueprint(main)


auth = Blueprint('auth', __name__)


class EditProductForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[NumberRange(min=0)])
    submit = SubmitField('Modify')


class AddProductForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description',
                              validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[NumberRange(min=0)])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Add Product')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Submit')


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'confirm_password', message='Passwords must match'), Length(min=6, max=15, message="Password must be at least 6 characters")])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    register = SubmitField('Register')


@ auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@ auth.route('/login', methods=['POST'])
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


@ auth.route('/signup')
def signup():
    form = RegisterForm()
    return render_template('signup.html', form=form)


@ auth.route('/signup', methods=['POST'])
def signup_post():
    form = RegisterForm()
    email = form.email.data
    phone = form.phone.data
    password = form.new_password.data
    name = form.name.data

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, phone=phone,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@ auth.route('/logout')
@ login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# blueprint for auth routes in our app
app.register_blueprint(auth)
