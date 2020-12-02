from app import db
from app import Product, User
db.create_all()

db.session.commit()