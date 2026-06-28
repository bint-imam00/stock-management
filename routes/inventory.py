"""Inventaire : vue du stock réel et ajustement manuel."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from extensions import db
from models import Product, Adjustment

bp = Blueprint("inventory", __name__, url_prefix="/inventory")


@bp.route("/")
@login_required
def list_view():
    items = Product.query.order_by(Product.name).all()
    return render_template("inventory/list.html", items=items)


@bp.route("/<int:product_id>/adjust", methods=["GET", "POST"])
@login_required
def adjust(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        try:
            new_quantity = int(request.form.get("new_quantity", "0"))
        except ValueError:
            new_quantity = -1
        reason = request.form.get("reason", "").strip() or "Ajustement manuel"

        if new_quantity < 0:
            flash("La nouvelle quantité doit être positive.", "danger")
            return render_template("inventory/adjust.html", product=product)

        if new_quantity == product.quantity:
            flash("Aucun changement détecté.", "info")
            return redirect(url_for("inventory.list_view"))

        adj = Adjustment(
            product_id=product.id,
            old_quantity=product.quantity,
            new_quantity=new_quantity,
            reason=reason,
        )
        product.quantity = new_quantity
        db.session.add(adj)
        db.session.commit()
        flash(f"Stock ajusté pour « {product.name} ».", "success")
        return redirect(url_for("inventory.list_view"))

    return render_template("inventory/adjust.html", product=product)


@bp.route("/history")
@login_required
def history():
    items = Adjustment.query.order_by(Adjustment.created_at.desc()).all()
    return render_template("inventory/history.html", items=items)
