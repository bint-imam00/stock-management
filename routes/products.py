"""CRUD des produits avec recherche."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Product, Category

bp = Blueprint("products", __name__, url_prefix="/products")


def _parse_form():
    """Lit et valide les champs du formulaire produit. Retourne (data, errors)."""
    errors = []
    name = request.form.get("name", "").strip()
    sku = request.form.get("sku", "").strip() or None
    category_id = request.form.get("category_id", type=int)
    try:
        price = float(request.form.get("price", "0") or 0)
    except ValueError:
        price = -1
    try:
        quantity = int(request.form.get("quantity", "0") or 0)
    except ValueError:
        quantity = -1
    try:
        min_stock = int(request.form.get("min_stock", "0") or 0)
    except ValueError:
        min_stock = -1

    if not name:
        errors.append("Le nom est requis.")
    if not category_id or not Category.query.get(category_id):
        errors.append("Une catégorie valide est requise.")
    if price < 0:
        errors.append("Le prix doit être positif.")
    if quantity < 0:
        errors.append("La quantité doit être positive.")
    if min_stock < 0:
        errors.append("Le stock minimum doit être positif.")

    return {
        "name": name,
        "sku": sku,
        "category_id": category_id,
        "price": price,
        "quantity": quantity,
        "min_stock": min_stock,
    }, errors


@bp.route("/")
@login_required
def list_view():
    q = request.args.get("q", "").strip()
    category_id = request.args.get("category_id", type=int)

    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)))
    if category_id:
        query = query.filter_by(category_id=category_id)

    items = query.order_by(Product.name).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "products/list.html",
        items=items,
        categories=categories,
        q=q,
        category_id=category_id,
    )


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    categories = Category.query.order_by(Category.name).all()
    if not categories:
        flash("Créez d'abord au moins une catégorie.", "warning")
        return redirect(url_for("categories.new"))

    if request.method == "POST":
        data, errors = _parse_form()
        if data["sku"] and Product.query.filter_by(sku=data["sku"]).first():
            errors.append("Ce SKU est déjà utilisé.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("products/form.html", item=None, categories=categories, form=data)
        db.session.add(Product(**data))
        db.session.commit()
        flash("Produit créé.", "success")
        return redirect(url_for("products.list_view"))
    return render_template("products/form.html", item=None, categories=categories, form=None)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(item_id):
    item = Product.query.get_or_404(item_id)
    categories = Category.query.order_by(Category.name).all()
    if request.method == "POST":
        data, errors = _parse_form()
        if data["sku"]:
            dup = Product.query.filter(Product.sku == data["sku"], Product.id != item.id).first()
            if dup:
                errors.append("Ce SKU est déjà utilisé.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("products/form.html", item=item, categories=categories, form=data)
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        flash("Produit mis à jour.", "success")
        return redirect(url_for("products.list_view"))
    return render_template("products/form.html", item=item, categories=categories, form=None)


@bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete(item_id):
    item = Product.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Produit supprimé.", "success")
    return redirect(url_for("products.list_view"))
