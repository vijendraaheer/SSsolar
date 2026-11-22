from . import db

class LoanSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    interest_rate = db.Column(db.Float, default=8.5)
    max_tenure_years = db.Column(db.Integer, default=20)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
