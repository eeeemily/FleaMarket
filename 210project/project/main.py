# main.py
import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from . import db as db


from project import auth, models

main = Blueprint('main', __name__)
# UPLOAD_FOLDER = os.path.join(current_app.root_path, 'instance', 'photos')


@main.route('/')
def index():
    from .models import Product
    return render_template('index.html', products=Product.query.all())


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    product_form = auth.AddProductForm()
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

        from .models import User
        author_id = User.query.filter_by(name=current_user.name).first().id

        # print("price =", price, "type = ", type(price))

        # print("got them")

        product = models.Product(title=title, description=description,
                                 price=price, photo_name=photo_name, author_id=author_id)
        # print("product created", title, description, price, photo_path)
        # print("product = ", product, product.title, product.description, product.price, product.photo_path)

        from .models import Product
        db.create_all()
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('profile.html', product_form=product_form, name=current_user.name)
