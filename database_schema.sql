-- WILD ERP Database Schema v3
-- SQLite

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT DEFAULT '',
    unit TEXT DEFAULT 'vnt',
    quantity REAL DEFAULT 1.0,
    price_without_vat REAL DEFAULT 0,
    supplier TEXT DEFAULT '',
    comment TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS configuration_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product_type TEXT NOT NULL CHECK(product_type IN ('hot_tub', 'sauna')),
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS configurations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product_type TEXT NOT NULL CHECK(product_type IN ('hot_tub', 'sauna')),
    category_id INTEGER,
    description TEXT DEFAULT '',
    base_material_cost REAL DEFAULT 0,
    base_labor_cost REAL DEFAULT 0,
    base_labor_hours REAL DEFAULT 0,
    b2b_price REAL DEFAULT 0,
    b2c_price REAL DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES configuration_categories(id)
);

CREATE TABLE IF NOT EXISTS configuration_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    configuration_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity REAL DEFAULT 1.0,
    is_optional INTEGER DEFAULT 0,
    FOREIGN KEY (configuration_id) REFERENCES configurations(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    client_order_number TEXT DEFAULT '',
    order_date TEXT DEFAULT (date('now')),
    country TEXT DEFAULT '',
    customer_name TEXT DEFAULT '',
    customer_address TEXT DEFAULT '',
    product_type TEXT DEFAULT '',
    status TEXT DEFAULT 'draft' CHECK(status IN ('draft','confirmed','production','completed','shipped','cancelled')),
    total_materials REAL DEFAULT 0,
    total_labor REAL DEFAULT 0,
    total_labor_hours REAL DEFAULT 0,
    total_cost REAL DEFAULT 0,
    total_price REAL DEFAULT 0,
    comment TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_type TEXT DEFAULT 'configuration',
    configuration_id INTEGER,
    name TEXT NOT NULL,
    name_production TEXT DEFAULT '',
    quantity REAL DEFAULT 1.0,
    material_cost REAL DEFAULT 0,
    labor_cost REAL DEFAULT 0,
    labor_hours REAL DEFAULT 0,
    total_cost REAL DEFAULT 0,
    unit_price REAL DEFAULT 0,
    total_price REAL DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    comment TEXT DEFAULT '',
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (configuration_id) REFERENCES configurations(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_materials_code ON materials(code);
CREATE INDEX IF NOT EXISTS idx_materials_category ON materials(category);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
