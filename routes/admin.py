
from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import func

from cloudinary_utils import delete_cloudinary_image, save_upload
from models import db
from models.business import BusinessRecord
from models.customer import Customer
from models.enquiry import Enquiry
from models.gallery import Gallery
from models.loan import LoanSetting
from models.office import Office
from models.project import Project
from models.scheme import Scheme
from models.service import Service
from models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Please login to access the Admin Panel.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    enquiries = Enquiry.query.count()
    customers = Customer.query.count()
    projects = Project.query.count()
    services = Service.query.count()

    revenue = 0.0
    records = BusinessRecord.query.order_by(
        BusinessRecord.year, BusinessRecord.id
    ).all()

    if records:
        revenue = sum(r.revenue or 0 for r in records)

    return render_template(
        "admin/dashboard.html",
        enquiries=enquiries,
        customers=customers,
        projects=projects,
        services=services,
        revenue=revenue,
        records=records,
    )


# =========================================================
# BUSINESS ANALYTICS
# =========================================================

@admin_bp.route("/analytics")
@admin_required
def analytics():
    records = BusinessRecord.query.order_by(
        BusinessRecord.year, BusinessRecord.id
    ).all()

    return render_template(
        "admin/analytics.html",
        records=records,
    )


@admin_bp.route("/business-records/add", methods=["GET", "POST"])
@admin_required
def add_business_record():
    if request.method == "POST":
        db.session.add(
            BusinessRecord(
                month=request.form.get("month", ""),
                year=int(request.form.get("year", 2026)),
                revenue=float(request.form.get("revenue", 0) or 0),
                enquiries=int(request.form.get("enquiries", 0) or 0),
                projects=int(request.form.get("projects", 0) or 0),
                installed_kw=float(request.form.get("installed_kw", 0) or 0),
            )
        )

        db.session.commit()
        flash("Business record added.", "success")
        return redirect(url_for("admin.analytics"))

    return render_template("admin/business_record_form.html")


# =========================================================
# CUSTOMERS
# =========================================================

@admin_bp.route("/customers")
@admin_required
def customers():
    confirmed_statuses = ["confirmed", "completed"]

    customers_list = (
        Customer.query
        .join(Enquiry, Enquiry.customer_id == Customer.id)
        .filter(func.lower(Enquiry.status).in_(confirmed_statuses))
        .distinct()
        .order_by(Customer.created_at.desc())
        .all()
    )

    return render_template(
        "admin/customers.html",
        customers=customers_list,
    )


@admin_bp.route("/customers/<int:customer_id>/delete", methods=["POST"])
@admin_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    try:
        # Preserve enquiry history by detaching the customer.
        Enquiry.query.filter_by(customer_id=customer.id).update(
            {Enquiry.customer_id: None},
            synchronize_session=False,
        )

        db.session.delete(customer)
        db.session.commit()

        flash("Customer deleted successfully.", "success")

    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "Could not delete customer id=%s", customer_id
        )
        flash(
            "Customer could not be deleted. Please check linked records and try again.",
            "error",
        )

    return redirect(url_for("admin.customers"))


# =========================================================
# ENQUIRIES
# =========================================================

@admin_bp.route("/enquiries")
@admin_required
def enquiries():
    enquiry_list = Enquiry.query.order_by(
        Enquiry.created_at.desc()
    ).all()

    return render_template(
        "admin/enquiries.html",
        enquiries=enquiry_list,
    )


@admin_bp.route("/enquiries/<int:enquiry_id>/status", methods=["POST"])
@admin_required
def enquiry_status(enquiry_id):
    enquiry = Enquiry.query.get_or_404(enquiry_id)

    enquiry.status = request.form.get("status", "New")
    db.session.commit()

    flash("Enquiry status updated.", "success")
    return redirect(url_for("admin.enquiries"))


# =========================================================
# PROJECTS
# =========================================================

@admin_bp.route("/projects")
@admin_required
def projects():
    project_list = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "admin/projects.html",
        projects=project_list,
    )


@admin_bp.route("/projects/add", methods=["GET", "POST"])
@admin_required
def add_project():
    if request.method == "POST":
        image = save_upload(
            request.files.get("image"),
            folder="ss-solar/projects",
        )

        project = Project(
            project_name=request.form.get("project_name", ""),
            customer_name=request.form.get("customer_name", ""),
            location=request.form.get("location", ""),
            system_size=request.form.get("system_size", ""),
            project_type=request.form.get("project_type", "Residential"),
            cost=request.form.get("cost", ""),
            installation_date=request.form.get("installation_date", ""),
            description=request.form.get("description", ""),
            image=image,
            featured=bool(request.form.get("featured")),
            status=request.form.get("status", "Completed"),
        )

        db.session.add(project)
        db.session.commit()

        flash("Project added successfully.", "success")
        return redirect(url_for("admin.projects"))

    return render_template(
        "admin/project_form.html",
        project=None,
    )


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Delete image from Cloudinary first.
    if project.image:
        delete_cloudinary_image(project.image)

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted.", "success")
    return redirect(url_for("admin.projects"))


# =========================================================
# SERVICES
# =========================================================

@admin_bp.route("/services")
@admin_required
def services():
    service_list = Service.query.order_by(
        Service.created_at.desc()
    ).all()

    return render_template(
        "admin/services.html",
        services=service_list,
    )


@admin_bp.route("/services/add", methods=["GET", "POST"])
@admin_required
def add_service():
    if request.method == "POST":
        image = save_upload(
            request.files.get("image"),
            folder="ss-solar/services",
        )

        db.session.add(
            Service(
                name=request.form.get("name", ""),
                description=request.form.get("description", ""),
                price=request.form.get("price", ""),
                image=image,
            )
        )

        db.session.commit()

        flash("Service added.", "success")
        return redirect(url_for("admin.services"))

    return render_template("admin/service_form.html")


@admin_bp.route("/services/<int:service_id>/delete", methods=["POST"])
@admin_required
def delete_service(service_id):
    item = Service.query.get_or_404(service_id)

    if item.image:
        delete_cloudinary_image(item.image)

    db.session.delete(item)
    db.session.commit()

    flash("Service deleted.", "success")
    return redirect(url_for("admin.services"))


# =========================================================
# GOVERNMENT SCHEMES
# =========================================================

@admin_bp.route("/schemes")
@admin_required
def schemes():
    scheme_list = Scheme.query.order_by(
        Scheme.created_at.desc()
    ).all()

    return render_template(
        "admin/schemes.html",
        schemes=scheme_list,
    )


@admin_bp.route("/schemes/add", methods=["GET", "POST"])
@admin_required
def add_scheme():
    if request.method == "POST":
        db.session.add(
            Scheme(
                name=request.form.get("name", ""),
                description=request.form.get("description", ""),
                eligibility=request.form.get("eligibility", ""),
                documents=request.form.get("documents", ""),
                subsidy_details=request.form.get("subsidy_details", ""),
                application_process=request.form.get("application_process", ""),
            )
        )

        db.session.commit()

        flash("Government scheme added.", "success")
        return redirect(url_for("admin.schemes"))

    return render_template("admin/scheme_form.html")


@admin_bp.route("/schemes/<int:scheme_id>/delete", methods=["POST"])
@admin_required
def delete_scheme(scheme_id):
    item = Scheme.query.get_or_404(scheme_id)

    db.session.delete(item)
    db.session.commit()

    flash("Scheme deleted.", "success")
    return redirect(url_for("admin.schemes"))


# =========================================================
# OFFICES
# =========================================================

@admin_bp.route("/offices")
@admin_required
def offices():
    office_list = Office.query.order_by(
        Office.created_at.desc()
    ).all()

    return render_template(
        "admin/offices.html",
        offices=office_list,
    )


@admin_bp.route("/offices/add", methods=["GET", "POST"])
@admin_required
def add_office():
    if request.method == "POST":
        image = save_upload(
            request.files.get("image"),
            folder="ss-solar/offices",
        )

        db.session.add(
            Office(
                office_name=request.form.get("office_name", ""),
                city=request.form.get("city", ""),
                address=request.form.get("address", ""),
                phone=request.form.get("phone", ""),
                email=request.form.get("email", ""),
                map_link=request.form.get("map_link", ""),
                image=image,
                opening_hours=request.form.get("opening_hours", ""),
            )
        )

        db.session.commit()

        flash("Office added.", "success")
        return redirect(url_for("admin.offices"))

    return render_template("admin/office_form.html")


@admin_bp.route("/offices/<int:office_id>/delete", methods=["POST"])
@admin_required
def delete_office(office_id):
    item = Office.query.get_or_404(office_id)

    if item.image:
        delete_cloudinary_image(item.image)

    db.session.delete(item)
    db.session.commit()

    flash("Office deleted.", "success")
    return redirect(url_for("admin.offices"))


# =========================================================
# GALLERY
# =========================================================

@admin_bp.route("/gallery")
@admin_required
def gallery():
    gallery_list = Gallery.query.order_by(
        Gallery.created_at.desc()
    ).all()

    return render_template(
        "admin/gallery.html",
        gallery=gallery_list,
    )


@admin_bp.route("/gallery/add", methods=["GET", "POST"])
@admin_required
def add_gallery():
    if request.method == "POST":
        image = save_upload(
            request.files.get("image"),
            folder="ss-solar/gallery",
        )

        if not image:
            flash("Please upload a valid image.", "error")
            return redirect(url_for("admin.add_gallery"))

        db.session.add(
            Gallery(
                title=request.form.get("title", ""),
                category=request.form.get(
                    "category", "Solar Installation"
                ),
                location=request.form.get("location", ""),
                image=image,
                description=request.form.get("description", ""),
            )
        )

        db.session.commit()

        flash("Gallery image added.", "success")
        return redirect(url_for("admin.gallery"))

    return render_template("admin/gallery_form.html")


@admin_bp.route("/gallery/<int:item_id>/delete", methods=["POST"])
@admin_required
def delete_gallery(item_id):
    item = Gallery.query.get_or_404(item_id)

    if item.image:
        delete_cloudinary_image(item.image)

    db.session.delete(item)
    db.session.commit()

    flash("Gallery image deleted.", "success")
    return redirect(url_for("admin.gallery"))


# =========================================================
# LOAN SETTINGS
# =========================================================

@admin_bp.route("/loan-settings", methods=["GET", "POST"])
@admin_required
def loan_settings():
    setting = LoanSetting.query.first()

    if request.method == "POST":
        setting.title = request.form.get("title", "Solar Loan")
        setting.description = request.form.get("description", "")
        setting.interest_rate = float(
            request.form.get("interest_rate", 8.5)
        )
        setting.max_tenure_years = int(
            request.form.get("max_tenure_years", 20)
        )

        db.session.commit()

        flash("Loan details updated.", "success")

    return render_template(
        "admin/loan_settings.html",
        setting=setting,
    )
