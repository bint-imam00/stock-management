"""Sorties de stock : retire du stock, avec vérification de disponibilité."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Product, StockOut

bp = Blueprint("stock_out", __name__, url_prefix="/stock-out")


@bp.route("/")
@login_required
def list_view():
    items = StockOut.query.order_by(StockOut.created_at.desc()).all()
    return render_template("stock_out/list.html", items=items)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    products = Product.query.order_by(Product.name).all()
    if not products:
        flash("Créez au moins un produit avant de saisir une sortie.", "warning")
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        product_id = request.form.get("product_id", type=int)
        try:
            quantity = int(request.form.get("quantity", "0") or 0)
        except ValueError:
            quantity = 0
        reason = request.form.get("reason", "").strip()

        product = Product.query.get(product_id) if product_id else None
        errors = []
        if not product:
            errors.append("Produit invalide.")
        if quantity <= 0:
            errors.append("La quantité doit être strictement positive.")
        if product and quantity > product.quantity:
            errors.append(
                f"Stock insuffisant : il reste {product.quantity} unité(s) de « {product.name} »."
            )

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("stock_out/form.html", products=products)

        entry = StockOut(product_id=product.id, quantity=quantity, reason=reason)
        product.quantity -= quantity
        db.session.add(entry)
        db.session.commit()
        flash(f"Sortie enregistrée (-{quantity} {product.name}).", "success")
        return redirect(url_for("stock_out.list_view"))

    return render_template("stock_out/form.html", products=products)
