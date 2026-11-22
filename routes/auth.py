from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username, role="admin").first()
        if user and user.check_password(password):
            session.clear()
            session["admin_id"] = user.id
            session["admin_username"] = user.username
            flash("Welcome to SS Solar Admin Panel.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid admin username or password.", "error")
    return render_template("admin/login.html")

@auth_bp.route("/admin/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
