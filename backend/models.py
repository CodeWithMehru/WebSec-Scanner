from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(1000), nullable=False)
