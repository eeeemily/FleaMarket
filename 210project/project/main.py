# main.py
import os

from flask import Blueprint, redirect, request, render_template, url_for, request, current_app
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
    from .models import Product, User
    return render_template('index.html', products=Product.query.all(), users=User)


@main.route('/test')
def test():
    from .models import Product
    return render_template('test.html', products=Product.query.all())


@main.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    from .models import Product, User
    product = Product.query.get_or_404(id)
    
    update_form = auth.EditProductForm(title=product.title, description=product.description, price=product.price)
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
    from .models import Product, User
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

        from .models import User, Product
        author_id = User.query.filter_by(name=current_user.name).first().id

        product = models.Product(title=title, description=description,
                                 price=price, photo_name=photo_name, author_id=author_id)
        
        db.create_all()
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('main.index'))


    from .models import Product
    return render_template('profile.html', product_form=product_form, name=current_user.name, products=Product.query.filter_by(author_id=current_user.id).all())
