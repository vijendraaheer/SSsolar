from . import db

class BusinessRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Float, default=0)
    enquiries = db.Column(db.Integer, default=0)
    projects = db.Column(db.Integer, default=0)
    installed_kw = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
