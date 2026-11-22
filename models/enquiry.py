
from . import db


class Enquiry(db.Model):
    __tablename__ = "enquiries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    email = db.Column(
        db.String(120)
    )

    requirement = db.Column(
        db.String(150)
    )

    message = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(40),
        default="New",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationship with Customer
    customer = db.relationship(
        "Customer",
        back_populates="enquiries"
    )