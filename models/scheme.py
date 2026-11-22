from . import db

class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    documents = db.Column(db.Text)
    subsidy_details = db.Column(db.Text)
    application_process = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
