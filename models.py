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
    metal=db.Column(db.Integer, nullable=False) # 0 is non-metal, 1 is semi-metal, 2 is metal, -1 is unsure (eg. for Og)?
    melting_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    boiling_point=db.Column(db.Float) # in Kelvin at 1 atmosphere of pressure
    radioactive=db.Column(db.Boolean) # if all isotopes are radioactive
    most_stable_isotope_found=db.Column(db.Integer) # eg. 97 for Technetium
    most_stable_halflife_found=db.Column(db.String(100)) # eg. 4.21±0.16 million years