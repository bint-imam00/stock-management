"""CRUD des fournisseurs."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Supplier

bp = Blueprint("suppliers", __name__, url_prefix="/suppliers")


def _parse_form():
    data = {
        "name": request.form.get("name", "").strip(),
        "contact": request.form.get("contact", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "address": request.form.get("address", "").strip(),
    }
    errors = []
    if not data["name"]:
        errors.append("Le nom du fournisseur est requis.")
    if data["email"] and "@" not in data["email"]:
        errors.append("Email invalide.")
    return data, errors


@bp.route("/")
@login_required
def list_view():
    items = Supplier.query.order_by(Supplier.name).all()
    return render_template("suppliers/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        data, errors = _parse_form()
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("suppliers/form.html", item=None, form=data)
        db.session.add(Supplier(**data))
        db.session.commit()
        flash("Fournisseur créé.", "success")
        return redirect(url_for("suppliers.list_view"))
    return render_template("suppliers/form.html", item=None, form=None)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id):
    item = Supplier.query.get_or_404(item_id)
    if request.method == "POST":
        data, errors = _parse_form()
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("suppliers/form.html", item=item, form=data)
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        flash("Fournisseur mis à jour.", "success")
        return redirect(url_for("suppliers.list_view"))
    return render_template("suppliers/form.html", item=item, form=None)


@bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete(item_id):
    item = Supplier.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Fournisseur supprimé.", "success")
    return redirect(url_for("suppliers.list_view"))
