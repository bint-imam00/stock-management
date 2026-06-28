"""Tableau de bord : indicateurs, alertes, graphiques."""
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from extensions import db
from models import Product, Category, Supplier, StockIn, StockOut

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/")
@login_required
def index():
    nb_products = Product.query.count()
    nb_categories = Category.query.count()
    nb_suppliers = Supplier.query.count()
    nb_stock_in = StockIn.query.count()
    nb_stock_out = StockOut.query.count()

    total_stock_value = db.session.query(
        func.coalesce(func.sum(Product.price * Product.quantity), 0)
    ).scalar() or 0

    out_of_stock = Product.query.filter(Product.quantity <= 0).all()
    low_stock = (
        Product.query.filter(Product.quantity > 0, Product.quantity <= Product.min_stock).all()
    )

    # Top 5 produits les plus vendus (selon sorties)
    top_sold = (
        db.session.query(
            Product.name,
            func.coalesce(func.sum(StockOut.quantity), 0).label("total"),
        )
        .join(StockOut, StockOut.product_id == Product.id)
        .group_by(Product.id)
        .order_by(func.sum(StockOut.quantity).desc())
        .limit(5)
        .all()
    )

    # Stock total par catégorie pour le graphique
    cat_stock = (
        db.session.query(Category.name, func.coalesce(func.sum(Product.quantity), 0))
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.id)
        .all()
    )

    return render_template(
        "dashboard.html",
        nb_products=nb_products,
        nb_categories=nb_categories,
        nb_suppliers=nb_suppliers,
        nb_stock_in=nb_stock_in,
        nb_stock_out=nb_stock_out,
        total_stock_value=total_stock_value,
        out_of_stock=out_of_stock,
        low_stock=low_stock,
        top_sold=top_sold,
        cat_stock=cat_stock,
    )
