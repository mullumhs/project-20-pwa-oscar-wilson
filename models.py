from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your database model here
# Example: class Item(db.Model):

class Element(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    symbol=db.Column(db.String(2), nullable=False)
    atomic_number=db.Column(db.Integer, nullable=False)
    atomic_weight=db.Column(db.Float, nullable=False)
    group=db.Column(db.Integer, nullable=False) # Group of 0 means it is in the f-block
    period=db.Column(db.Integer, nullable=False)
    x_coord=db.Column(db.Integer, nullable=False)
    y_coord=db.Column(db.Integer, nullable=False)
    metal=db.Column(db.String(100), nullable=False) # Non-Metal, Semi-Metal, Metal, Unsure
    melting_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    boiling_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    radioactive=db.Column(db.Boolean) # if all isotopes are radioactive
    most_stable_isotope_found=db.Column(db.Integer) # eg. 97 for Technetium
    most_stable_halflife_found=db.Column(db.String(100)) # eg. 4.21±0.16 million years