"""Script de seed : crée un utilisateur admin et des données de démonstration."""
from datetime import datetime, timedelta
import random

from app import app
from extensions import db
from models import User, Category, Supplier, Product, StockIn, StockOut


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # -- Utilisateur admin --
        admin = User(username="admin", full_name="Administrateur")
        admin.set_password("admin123")
        db.session.add(admin)

        # -- Catégories --
        categories_data = [
            ("Boissons", "Boissons gazeuses, jus, eaux"),
            ("Alimentation", "Produits alimentaires de base"),
            ("Hygiène", "Produits d'hygiène et beauté"),
            ("Électronique", "Petits accessoires électroniques"),
            ("Fournitures", "Fournitures de bureau"),
        ]
        categories = []
        for name, desc in categories_data:
            c = Category(name=name, description=desc)
            db.session.add(c)
            categories.append(c)
        db.session.flush()

        # -- Fournisseurs --
        suppliers_data = [
            ("SENEGAL DISTRIBUTION", "M. Diop", "contact@sendistrib.sn", "+221 33 821 00 00", "Dakar, Sénégal"),
            ("WEST AFRICA TRADING", "Mme Ndiaye", "info@watrading.com", "+221 77 100 22 33", "Pikine, Sénégal"),
            ("GLOBAL FOODS", "M. Sow", "contact@globalfoods.sn", "+221 78 500 11 22", "Thiès, Sénégal"),
            ("TECH IMPORT", "M. Faye", "ventes@techimport.sn", "+221 77 999 88 77", "Dakar, Sénégal"),
        ]
        suppliers = []
        for name, contact, email, phone, address in suppliers_data:
            s = Supplier(name=name, contact=contact, email=email, phone=phone, address=address)
            db.session.add(s)
            suppliers.append(s)
        db.session.flush()

        # -- Produits --
        products_data = [
            # (nom, sku, idx catégorie, prix, qté, stock min)
            ("Coca-Cola 1.5L", "BOI-001", 0, 1200, 80, 30),
            ("Eau Kirène 1.5L", "BOI-002", 0, 500, 150, 50),
            ("Jus d'orange Pressea 1L", "BOI-003", 0, 1500, 20, 25),
            ("Riz parfumé 5kg", "ALI-001", 1, 5500, 40, 20),
            ("Huile d'arachide 5L", "ALI-002", 1, 8500, 5, 15),
            ("Sucre 1kg", "ALI-003", 1, 900, 0, 30),
            ("Savon Dove 100g", "HYG-001", 2, 750, 60, 25),
            ("Dentifrice Colgate", "HYG-002", 2, 1200, 35, 20),
            ("Shampoing 400ml", "HYG-003", 2, 2500, 18, 10),
            ("Câble USB-C", "ELE-001", 3, 3500, 25, 10),
            ("Écouteurs filaires", "ELE-002", 3, 4500, 3, 8),
            ("Chargeur secteur 20W", "ELE-003", 3, 7500, 12, 5),
            ("Cahier 200 pages", "FOU-001", 4, 800, 100, 40),
            ("Stylo bille bleu", "FOU-002", 4, 150, 250, 80),
            ("Ramette papier A4", "FOU-003", 4, 4500, 8, 10),
        ]
        products = []
        for name, sku, cat_idx, price, qty, mn in products_data:
            p = Product(
                name=name, sku=sku, category_id=categories[cat_idx].id,
                price=price, quantity=qty, min_stock=mn,
            )
            db.session.add(p)
            products.append(p)
        db.session.flush()

        # -- Entrées de stock historiques --
        for _ in range(25):
            p = random.choice(products)
            s = random.choice(suppliers)
            qty = random.randint(10, 80)
            unit_price = round(p.price * random.uniform(0.6, 0.85), 2)
            days_ago = random.randint(1, 60)
            entry = StockIn(
                product_id=p.id, supplier_id=s.id, quantity=qty,
                unit_price=unit_price, note=f"BL-{random.randint(1000,9999)}",
                created_at=datetime.utcnow() - timedelta(days=days_ago),
            )
            db.session.add(entry)

        # -- Sorties de stock historiques --
        reasons = ["Vente", "Vente", "Vente", "Vente", "Casse", "Transfert"]
        for _ in range(40):
            p = random.choice(products)
            qty = random.randint(1, 8)
            days_ago = random.randint(1, 45)
            exit_ = StockOut(
                product_id=p.id, quantity=qty, reason=random.choice(reasons),
                created_at=datetime.utcnow() - timedelta(days=days_ago),
            )
            db.session.add(exit_)

        db.session.commit()

        print("Base de données initialisée :")
        print(f"  - {User.query.count()} utilisateur (admin / admin123)")
        print(f"  - {Category.query.count()} catégories")
        print(f"  - {Supplier.query.count()} fournisseurs")
        print(f"  - {Product.query.count()} produits")
        print(f"  - {StockIn.query.count()} entrées de stock")
        print(f"  - {StockOut.query.count()} sorties de stock")


if __name__ == "__main__":
    run()
