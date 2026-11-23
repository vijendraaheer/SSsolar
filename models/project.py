from . import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(160), nullable=False)
    customer_name = db.Column(db.String(120))
    location = db.Column(db.String(160))
    system_size = db.Column(db.String(60))
    project_type = db.Column(db.String(80))
    cost = db.Column(db.String(100))
    installation_date = db.Column(db.String(40))
    description = db.Column(db.Text)
    image = db.Column(db.String(1000))
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(40), default="Completed")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
