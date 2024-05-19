from app import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID string format
    username = db.Column(db.String(80), unique=True, nullable=False)
