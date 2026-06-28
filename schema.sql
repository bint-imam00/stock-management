-- Script SQL de référence (généré automatiquement par SQLAlchemy au démarrage).
-- Conservé pour documentation et déploiement manuel éventuel.

CREATE TABLE users (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    username     VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name    VARCHAR(120),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(80) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE suppliers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(120) NOT NULL,
    contact    VARCHAR(120),
    email      VARCHAR(120),
    phone      VARCHAR(40),
    address    VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         VARCHAR(120) NOT NULL,
    sku          VARCHAR(40) UNIQUE,
    category_id  INTEGER NOT NULL REFERENCES categories(id),
    price        REAL NOT NULL DEFAULT 0,
    quantity     INTEGER NOT NULL DEFAULT 0,
    min_stock    INTEGER NOT NULL DEFAULT 0,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_in (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL REFERENCES products(id),
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    quantity    INTEGER NOT NULL,
    unit_price  REAL DEFAULT 0,
    note        VARCHAR(255),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_out (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL,
    reason     VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE adjustments (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   INTEGER NOT NULL REFERENCES products(id),
    old_quantity INTEGER NOT NULL,
    new_quantity INTEGER NOT NULL,
    reason       VARCHAR(255),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
);
