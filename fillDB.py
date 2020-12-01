from app import db
from app import Products, Users
db.create_all()

db.session.commit()