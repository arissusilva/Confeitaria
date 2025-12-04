from main import db
from flask_login import UserMixin

class User (db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key=True)
    nome = db.Column (db.String (120), nullable = False)
    email = db.Column (db.String(120), unique = True, nullable= False)
    senha = db.Column (db.String(120), nullable = False)