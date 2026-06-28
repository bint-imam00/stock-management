"""Authentification : connexion / déconnexion."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Veuillez renseigner tous les champs.", "danger")
            return render_template("auth/login.html")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Identifiants invalides.", "danger")
            return render_template("auth/login.html")

        login_user(user)
        flash(f"Bienvenue {user.full_name or user.username} !", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("auth.login"))
