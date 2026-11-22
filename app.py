from pathlib import Path

from flask import Flask

from config import Config
from models import db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.public import public_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.root_path, "database").mkdir(parents=True, exist_ok=True)


    db.init_app(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        from models.gallery import Gallery
        from models.loan import LoanSetting
        from models.office import Office
        from models.project import Project
        from models.scheme import Scheme
        from models.service import Service
        from models.user import User

        db.create_all()

        if not User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first():
            db.session.add(User(
                username=app.config["ADMIN_USERNAME"],
                password=app.config["ADMIN_PASSWORD"],
                role="admin"
            ))

        if Service.query.count() == 0:
            defaults = [
                ("Residential Solar", "Rooftop solar solutions for homes with clean, reliable power.", "Starting consultation"),
                ("Commercial Solar", "Solar systems designed for shops, offices and commercial buildings.", "Custom quotation"),
                ("Industrial Solar", "High-capacity solar solutions for industrial energy requirements.", "Custom quotation"),
                ("On-Grid Solar", "Grid-connected solar systems for reducing electricity bills.", "Site survey required"),
                ("Off-Grid Solar", "Battery-backed solar systems for locations needing energy independence.", "Custom quotation"),
                ("Hybrid Solar", "Solar + grid + battery solutions for flexible power management.", "Custom quotation"),
                ("Solar Water Pump", "Solar-powered water pumping solutions for agricultural use.", "Custom quotation"),
                ("Solar AMC", "Maintenance and support for existing solar installations.", "Service plan"),
            ]
            db.session.add_all([Service(name=n, description=d, price=p) for n, d, p in defaults])

        if Scheme.query.count() == 0:
            db.session.add(Scheme(
                name="PM Surya Ghar / Rooftop Solar",
                description="Government rooftop-solar scheme information can be published and updated here by the administrator.",
                eligibility="Add current eligibility conditions from the official government notification.",
                documents="Aadhaar/identity documents, electricity bill, bank details and other documents as applicable.",
                subsidy_details="Subsidy information is editable from the Admin Panel so published values can be kept current.",
                application_process="Update the application steps according to the latest official process."
            ))

        if Office.query.count() == 0:
            db.session.add(Office(
                office_name="SS Solar Solutions - Kota",
                city="Kota",
                address="27 B-Block Parshavnath City, Kunhadi, Kota 324008",
                phone="9950855563",
                email="sssolarsolutions1@gmail.com",
                opening_hours="Mon-Sat: 9:00 AM - 7:00 PM"
            ))

        if LoanSetting.query.count() == 0:
            db.session.add(LoanSetting(
                title="Solar Loan",
                description="Indicative solar-loan calculator. Final interest rate, eligibility, processing fee and approval are subject to the lender.",
                interest_rate=8.5,
                max_tenure_years=20
            ))

        db.session.commit()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
