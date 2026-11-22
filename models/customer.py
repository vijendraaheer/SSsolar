
from datetime import datetime

from models import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    city = db.Column(
        db.String(100),
        nullable=True
    )

    solar_type = db.Column(
        db.String(50),
        nullable=True,
        default="Residential"
    )

    capacity = db.Column(
        db.String(50),
        nullable=True
    )

    address = db.Column(
        db.Text,
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Linked enquiries for this customer
    enquiries = db.relationship(
        "Enquiry",
        back_populates="customer",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Customer {self.name}>"