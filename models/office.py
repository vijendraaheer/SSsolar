
from . import db


class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String(160), nullable=False)
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    map_link = db.Column(db.String(500))
    image = db.Column(db.String(1000))
    opening_hours = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
