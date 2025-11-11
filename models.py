from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class Element(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    symbol=db.Column(db.String(2), nullable=False)
    group=db.Column(db.Integer, nullable=False)
    period=db.Column(db.Integer, nullable=False)
    melting_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    boiling_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    radioactive=db.Column(db.Boolean) # if all isotopes are radioactive