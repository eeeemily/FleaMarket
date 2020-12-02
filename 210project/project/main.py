# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, EqualTo, Email, Length 
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


class AddProductForm(FlaskForm):
    product_title = StringField ('Product Name', validators=[DataRequired()])
    product_description = StringField ('Product Description', validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Add Product')

@main.route('/profile')
@login_required
def profile():
    product_form = AddProductForm()
    if product_form.validate_on_submit():
        photo = product_form.photo.data
        filename = photo.filename
        photo.save(os.path.join(app.instance_path, 'photos', filename))

        title = product_form.product_title.data
        description = product_form.product_description.data
        photo_path = os.path.join(app.instance_path, 'photos', filename)
        
        product = Products(title=title, description=description, photo_path=photo_path)
        print("product created", title, description, photo_path)
        db.session.add(product)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    return render_template('profile.html', product_form=product_form, name=current_user.name)

   