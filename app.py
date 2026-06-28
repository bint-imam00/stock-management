"""Point d'entrée de l'application Flask de gestion de stock."""
from flask import Flask, redirect, url_for
from flask_login import current_user

from config import Config
from extensions import db, login_manager
import models  # noqa: F401  (enregistre les modèles)
from routes.auth import bp as auth_bp
from routes.dashboard import bp as dashboard_bp
from routes.categories import bp as categories_bp
from routes.products import bp as products_bp
from routes.suppliers import bp as suppliers_bp
from routes.stock_in import bp as stock_in_bp
from routes.stock_out import bp as stock_out_bp
from routes.inventory import bp as inventory_bp
from routes.reports import bp as reports_bp


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    for bp in (
        auth_bp,
        dashboard_bp,
        categories_bp,
        products_bp,
        suppliers_bp,
        stock_in_bp,
        stock_out_bp,
        inventory_bp,
        reports_bp,
    ):
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def not_found(_e):
        return ("Page introuvable", 404)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
