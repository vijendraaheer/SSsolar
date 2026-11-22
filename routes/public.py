from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.project import Project
from models.service import Service
from models.scheme import Scheme
from models.office import Office
from models.gallery import Gallery
from models.customer import Customer
from models.enquiry import Enquiry
from models.loan import LoanSetting

public_bp = Blueprint("public", __name__)

CONTACT = {
    "company": "SS Solar Solutions",
    "owner": "Jitendra Goswami",
    "phone1": "9950855563",
    "phone2": "7891021268",
    "email": "sssolarsolutions1@gmail.com",
    "address": "27 B-Block Parshavnath City, Kunhadi, Kota 324008",
    "instagram": "ss_solarsolutions",
}

@public_bp.app_context_processor
def inject_global():
    return {"contact": CONTACT}

@public_bp.route("/")
def home():
    featured = Project.query.filter_by(featured=True, status="Completed").order_by(Project.created_at.desc()).limit(6).all()
    if not featured:
        featured = Project.query.order_by(Project.created_at.desc()).limit(6).all()
    services = Service.query.filter_by(status=True).order_by(Service.created_at.desc()).limit(6).all()
    schemes = Scheme.query.filter_by(status=True).order_by(Scheme.created_at.desc()).limit(3).all()
    return render_template("customer/index.html", featured=featured, services=services, schemes=schemes)

@public_bp.route("/about")
def about():
    return render_template("customer/about.html")

@public_bp.route("/services")
def services():
    return render_template("customer/services.html", services=Service.query.filter_by(status=True).all())

@public_bp.route("/schemes")
def schemes():
    return render_template("customer/schemes.html", schemes=Scheme.query.filter_by(status=True).all())

@public_bp.route("/loans", methods=["GET", "POST"])
def loans():
    setting = LoanSetting.query.first()
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))
            rate = float(request.form.get("rate", setting.interest_rate if setting else 8.5))
            years = int(request.form.get("years", 5))
            months = years * 12
            monthly_rate = rate / 12 / 100
            emi = amount / months if monthly_rate == 0 else amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
            total = emi * months
            result = {"emi": round(emi, 2), "interest": round(total - amount, 2), "total": round(total, 2)}
        except (TypeError, ValueError, ZeroDivisionError):
            flash("Please enter valid loan details.", "error")
    return render_template("customer/loans.html", setting=setting, result=result)

@public_bp.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        try:
            monthly_bill = float(request.form.get("monthly_bill", 0))
            tariff = float(request.form.get("tariff", 8))
            generation_per_kw = float(request.form.get("generation_per_kw", 120))
            if monthly_bill <= 0 or tariff <= 0 or generation_per_kw <= 0:
                raise ValueError
            monthly_units = monthly_bill / tariff
            system_kw = monthly_units / generation_per_kw
            annual_units = system_kw * generation_per_kw * 12
            annual_saving = annual_units * tariff
            result = {
                "monthly_units": round(monthly_units),
                "system_kw": round(system_kw, 2),
                "annual_units": round(annual_units),
                "annual_saving": round(annual_saving),
            }
        except (TypeError, ValueError):
            flash("Please enter valid positive numbers.", "error")
    return render_template("customer/calculator.html", result=result)

@public_bp.route("/projects")
def projects():
    return render_template("customer/projects.html", projects=Project.query.order_by(Project.created_at.desc()).all())

@public_bp.route("/projects/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("customer/project_detail.html", project=project)

@public_bp.route("/gallery")
def gallery():
    category = request.args.get("category", "All")
    query = Gallery.query
    if category != "All":
        query = query.filter_by(category=category)
    return render_template("customer/gallery.html", gallery=query.order_by(Gallery.created_at.desc()).all(), category=category)

@public_bp.route("/offices")
def offices():
    return render_template("customer/offices.html", offices=Office.query.order_by(Office.created_at.desc()).all())

@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        requirement = request.form.get("requirement", "").strip()
        message = request.form.get("message", "").strip()
        city = request.form.get("city", "").strip()

        if not name or not phone:
            flash("Name and phone are required.", "error")
            return redirect(url_for("public.contact"))

        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            customer = Customer(name=name, phone=phone, email=email, city=city)
            db.session.add(customer)
            db.session.flush()

        enquiry = Enquiry(
            customer_id=customer.id,
            name=name,
            phone=phone,
            email=email,
            requirement=requirement,
            message=message,
            status="New",
        )
        db.session.add(enquiry)
        db.session.commit()
        flash("Thank you! Your enquiry has been received. We will contact you soon.", "success")
        return redirect(url_for("public.contact"))

    return render_template("customer/contact.html")

@public_bp.route("/health")
def health():
    return {"status": "ok"}
