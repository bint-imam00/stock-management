# StockApp — Application web de gestion de stock

Application Flask complète pour la gestion d'un stock : catégories, produits, fournisseurs, entrées, sorties, inventaire, alertes, rapports et exports Excel.

## Fonctionnalités

- **Authentification** : login / logout, accès protégé.
- **Dashboard** : indicateurs, graphiques (Chart.js), alertes rupture / sous-stock.
- **Catégories** : CRUD complet.
- **Produits** : CRUD avec recherche par nom/SKU, filtre par catégorie, stock minimum.
- **Fournisseurs** : CRUD complet.
- **Entrées de stock** : sélection fournisseur + produit, mise à jour automatique du stock, historique.
- **Sorties de stock** : avec vérification de la disponibilité, historique.
- **Inventaire** : stock réel et ajustement manuel (traçabilité des ajustements).
- **Alertes** : produits en rupture, produits sous seuil minimum.
- **Rapports** : état du stock, mouvements filtrables par période, top ventes.
- **Exports Excel** (`.xlsx`) du stock et des mouvements.

## Stack technique

- **Backend** : Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login
- **Base de données** : SQLite (relationnelle, fichier `stock.db`)
- **Frontend** : Bootstrap 5, Bootstrap Icons, Chart.js (CDN)
- **Export** : openpyxl

## Architecture

```
Projet_Aliou/
├── app.py                  # Application factory + point d'entrée
├── config.py               # Configuration
├── extensions.py           # Instances SQLAlchemy / LoginManager
├── models.py               # Modèles (User, Category, Product, Supplier, StockIn, StockOut, Adjustment)
├── seed.py                 # Initialisation BD + données de démo
├── schema.sql              # Script SQL de référence
├── requirements.txt
├── routes/                 # Contrôleurs (un blueprint par module)
│   ├── auth.py
│   ├── dashboard.py
│   ├── categories.py
│   ├── products.py
│   ├── suppliers.py
│   ├── stock_in.py
│   ├── stock_out.py
│   ├── inventory.py
│   └── reports.py
├── templates/              # Vues Jinja2
│   ├── base.html
│   ├── auth/login.html
│   ├── dashboard.html
│   └── <module>/{list,form}.html
└── static/css/style.css
```

Architecture MVC :
- **Model** : `models.py`
- **View** : `templates/`
- **Controller** : `routes/`

## Installation et lancement (Windows)

### 1. Créer un environnement virtuel

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

### 3. Initialiser la base avec les données de test

```powershell
python seed.py
```

Cela crée le fichier `stock.db` (SQLite) avec :
- 1 utilisateur **admin** / **admin123**
- 5 catégories, 4 fournisseurs, 15 produits
- 25 entrées et 40 sorties historiques

### 4. Lancer l'application

```powershell
python app.py
```

Ouvrir [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Utilisation rapide

1. Connectez-vous : `admin` / `admin123`.
2. Le dashboard affiche les indicateurs, graphiques et alertes.
3. Naviguez via la barre du haut : Catégories → Produits → Fournisseurs → Entrées → Sorties → Inventaire → Rapports.
4. Rapports : filtrez par période, exportez en Excel.

## Sécurité

- Mots de passe hachés (Werkzeug).
- Toutes les pages (sauf `/auth/login`) protégées par `@login_required`.
- Validation des formulaires côté serveur.

## Réinitialiser la base

```powershell
python seed.py
```

(le script supprime et recrée toutes les tables).

## Configuration

Variables d'environnement supportées :
- `SECRET_KEY` : clé Flask (par défaut une valeur de dev).
- `DATABASE_URL` : URL SQLAlchemy (par défaut `sqlite:///stock.db`). Pour PostgreSQL :

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://user:pwd@host/dbname"
```
