"""Entrées de stock : ajoute du stock à un produit depuis un fournisseur."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Product, Supplier, StockIn

bp = Blueprint("stock_in", __name__, url_prefix="/stock-in")


@bp.route("/")
@login_required
def list_view():
    items = StockIn.query.order_by(StockIn.created_at.desc()).all()
    return render_template("stock_in/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    products = Product.query.order_by(Product.name).all()
    suppliers = Supplier.query.order_by(Supplier.name).all()

    if not products or not suppliers:
        flash("Créez au moins un produit et un fournisseur avant de saisir une entrée.", "warning")
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        product_id = request.form.get("product_id", type=int)
        supplier_id = request.form.get("supplier_id", type=int)
        try:
            quantity = int(request.form.get("quantity", "0") or 0)
        except ValueError:
            quantity = 0
        try:
            unit_price = float(request.form.get("unit_price", "0") or 0)
        except ValueError:
            unit_price = -1
        note = request.form.get("note", "").strip()

        errors = []
        product = Product.query.get(product_id) if product_id else None
        supplier = Supplier.query.get(supplier_id) if supplier_id else None
        if not product:
            errors.append("Produit invalide.")
        if not supplier:
            errors.append("Fournisseur invalide.")
        if quantity <= 0:
            errors.append("La quantité doit être strictement positive.")
        if unit_price < 0:
            errors.append("Le prix unitaire doit être positif.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("stock_in/form.html", products=products, suppliers=suppliers)

        entry = StockIn(
            product_id=product.id,
            supplier_id=supplier.id,
            quantity=quantity,
            unit_price=unit_price,
            note=note,
        )
        product.quantity += quantity
        db.session.add(entry)
        db.session.commit()
        flash(f"Entrée de stock enregistrée (+{quantity} {product.name}).", "success")
        return redirect(url_for("stock_in.list_view"))

    return render_template("stock_in/form.html", products=products, suppliers=suppliers)
