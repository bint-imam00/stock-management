"""CRUD des catégories."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Category

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.route("/")
@login_required
def list_view():
    items = Category.query.order_by(Category.name).all()
    return render_template("categories/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if not name:
            flash("Le nom est requis.", "danger")
            return render_template("categories/form.html", item=None)
        if Category.query.filter_by(name=name).first():
            flash("Cette catégorie existe déjà.", "danger")
            return render_template("categories/form.html", item=None)
        db.session.add(Category(name=name, description=description))
        db.session.commit()
        flash("Catégorie créée avec succès.", "success")
        return redirect(url_for("categories.list_view"))
    return render_template("categories/form.html", item=None)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id):
    item = Category.query.get_or_404(item_id)
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Le nom est requis.", "danger")
            return render_template("categories/form.html", item=item)
        duplicate = Category.query.filter(Category.name == name, Category.id != item.id).first()
        if duplicate:
            flash("Cette catégorie existe déjà.", "danger")
            return render_template("categories/form.html", item=item)
        item.name = name
        item.description = request.form.get("description", "").strip()
        db.session.commit()
        flash("Catégorie mise à jour.", "success")
        return redirect(url_for("categories.list_view"))
    return render_template("categories/form.html", item=item)


@bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete(item_id):
    item = Category.query.get_or_404(item_id)
    if item.products:
        flash("Impossible de supprimer : des produits sont rattachés à cette catégorie.", "danger")
        return redirect(url_for("categories.list_view"))
    db.session.delete(item)
    db.session.commit()
    flash("Catégorie supprimée.", "success")
    return redirect(url_for("categories.list_view"))
