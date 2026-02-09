"""
WILD ERP System - Backend API
Flask application for managing hot tubs and saunas production
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

DATABASE = 'wild_erp.db'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return db

def init_db():
    """Initialize database with schema"""
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            with open('database_schema.sql', 'r', encoding='utf-8') as f:
                db.executescript(f.read())
            db.commit()
            print("Database initialized successfully!")

# ==============================================================================
# MATERIALS (ŽALIAVOS) ENDPOINTS
# ==============================================================================

@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get all materials with optional filtering"""
    db = get_db()
    
    # Get query parameters
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = "SELECT * FROM materials WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    if search:
        query += " AND (code LIKE ? OR name LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += " ORDER BY code"
    
    materials = db.execute(query, params).fetchall()
    
    return jsonify([dict(m) for m in materials])

@app.route('/api/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Get single material by ID"""
    db = get_db()
    material = db.execute("SELECT * FROM materials WHERE id = ?", (material_id,)).fetchone()
    
    if material is None:
        return jsonify({"error": "Material not found"}), 404
    
    return jsonify(dict(material))

@app.route('/api/materials', methods=['POST'])
def create_material():
    """Create new material"""
    data = request.json
    db = get_db()
    
    try:
        cursor = db.execute("""
            INSERT INTO materials 
            (code, name, category, unit, quantity, price_without_vat, supplier, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['code'],
            data['name'],
            data.get('category', ''),
            data['unit'],
            data.get('quantity', 1.0),
            data['price_without_vat'],
            data.get('supplier', ''),
            data.get('comment', '')
        ))
        db.commit()
        
        return jsonify({"id": cursor.lastrowid, "message": "Material created successfully"}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Material code already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/materials/<int:material_id>', methods=['PUT'])
def update_material(material_id):
    """Update existing material"""
    data = request.json
    db = get_db()
    
    try:
        db.execute("""
            UPDATE materials 
            SET name = ?, category = ?, unit = ?, quantity = ?, 
                price_without_vat = ?, supplier = ?, comment = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            data['name'],
            data.get('category', ''),
            data['unit'],
            data.get('quantity', 1.0),
            data['price_without_vat'],
            data.get('supplier', ''),
            data.get('comment', ''),
            material_id
        ))
        db.commit()
        
        if db.total_changes == 0:
            return jsonify({"error": "Material not found"}), 404
        
        return jsonify({"message": "Material updated successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/materials/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    """Delete material"""
    db = get_db()
    
    db.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    db.commit()
    
    if db.total_changes == 0:
        return jsonify({"error": "Material not found"}), 404
    
    return jsonify({"message": "Material deleted successfully"})

@app.route('/api/materials/categories', methods=['GET'])
def get_material_categories():
    """Get unique material categories"""
    db = get_db()
    categories = db.execute("""
        SELECT DISTINCT category 
        FROM materials 
        WHERE category IS NOT NULL AND category != ''
        ORDER BY category
    """).fetchall()
    
    return jsonify([c['category'] for c in categories])

# ==============================================================================
# CONFIGURATIONS (KOMPLEKTACIJOS) ENDPOINTS
# ==============================================================================

@app.route('/api/configurations', methods=['GET'])
def get_configurations():
    """Get all configurations"""
    db = get_db()
    
    product_type = request.args.get('type')  # 'hot_tub' or 'sauna'
    category_id = request.args.get('category_id')
    
    query = """
        SELECT c.*, cat.name as category_name
        FROM configurations c
        LEFT JOIN configuration_categories cat ON c.category_id = cat.id
        WHERE c.is_active = 1
    """
    params = []
    
    if product_type:
        query += " AND c.product_type = ?"
        params.append(product_type)
    
    if category_id:
        query += " AND c.category_id = ?"
        params.append(category_id)
    
    query += " ORDER BY cat.sort_order, c.name"
    
    configs = db.execute(query, params).fetchall()
    
    return jsonify([dict(c) for c in configs])

@app.route('/api/configurations/<int:config_id>', methods=['GET'])
def get_configuration(config_id):
    """Get configuration with materials"""
    db = get_db()
    
    config = db.execute("""
        SELECT c.*, cat.name as category_name
        FROM configurations c
        LEFT JOIN configuration_categories cat ON c.category_id = cat.id
        WHERE c.id = ?
    """, (config_id,)).fetchone()
    
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    
    materials = db.execute("""
        SELECT cm.*, m.code, m.name as material_name, m.unit
        FROM configuration_materials cm
        JOIN materials m ON cm.material_id = m.id
        WHERE cm.configuration_id = ?
    """, (config_id,)).fetchall()
    
    result = dict(config)
    result['materials'] = [dict(m) for m in materials]
    
    return jsonify(result)

# ==============================================================================
# ORDERS (UŽSAKYMAI) ENDPOINTS
# ==============================================================================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    db = get_db()
    
    status = request.args.get('status')
    product_type = request.args.get('type')
    
    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if product_type:
        query += " AND product_type = ?"
        params.append(product_type)
    
    query += " ORDER BY order_date DESC, id DESC"
    
    orders = db.execute(query, params).fetchall()
    
    return jsonify([dict(o) for o in orders])

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order with all items"""
    db = get_db()
    
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    items = db.execute("""
        SELECT * FROM order_items 
        WHERE order_id = ? 
        ORDER BY sort_order, id
    """, (order_id,)).fetchall()
    
    result = dict(order)
    result['items'] = [dict(i) for i in items]
    
    return jsonify(result)

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    data = request.json
    db = get_db()
    
    try:
        cursor = db.execute("""
            INSERT INTO orders 
            (order_number, client_order_number, order_date, country, 
             customer_name, customer_address, product_type, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['order_number'],
            data.get('client_order_number', ''),
            data.get('order_date', datetime.now().strftime('%Y-%m-%d')),
            data.get('country', 'LT'),
            data.get('customer_name', ''),
            data.get('customer_address', ''),
            data['product_type'],
            data.get('status', 'draft')
        ))
        db.commit()
        
        return jsonify({"id": cursor.lastrowid, "message": "Order created successfully"}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": "Order number already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>/items', methods=['POST'])
def add_order_item(order_id):
    """Add item to order"""
    data = request.json
    db = get_db()
    
    try:
        cursor = db.execute("""
            INSERT INTO order_items 
            (order_id, item_type, configuration_id, name, name_production,
             quantity, material_cost, labor_cost, labor_hours, 
             total_cost, unit_price, total_price, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            data['item_type'],
            data.get('configuration_id'),
            data['name'],
            data.get('name_production', ''),
            data.get('quantity', 1.0),
            data.get('material_cost', 0),
            data.get('labor_cost', 0),
            data.get('labor_hours', 0),
            data.get('total_cost', 0),
            data.get('unit_price', 0),
            data.get('total_price', 0),
            data.get('comment', '')
        ))
        db.commit()
        
        # Recalculate order totals
        recalculate_order_totals(db, order_id)
        
        return jsonify({"id": cursor.lastrowid, "message": "Item added successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def recalculate_order_totals(db, order_id):
    """Recalculate order totals based on items"""
    totals = db.execute("""
        SELECT 
            SUM(material_cost * quantity) as total_materials,
            SUM(labor_cost * quantity) as total_labor,
            SUM(labor_hours * quantity) as total_labor_hours,
            SUM(total_cost * quantity) as total_cost,
            SUM(total_price * quantity) as total_price
        FROM order_items
        WHERE order_id = ?
    """, (order_id,)).fetchone()
    
    db.execute("""
        UPDATE orders 
        SET total_materials = ?,
            total_labor = ?,
            total_labor_hours = ?,
            total_cost = ?,
            total_price = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        totals['total_materials'] or 0,
        totals['total_labor'] or 0,
        totals['total_labor_hours'] or 0,
        totals['total_cost'] or 0,
        totals['total_price'] or 0,
        order_id
    ))
    db.commit()

# ==============================================================================
# UTILITY ENDPOINTS
# ==============================================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    db = get_db()
    
    stats = {
        'materials_count': db.execute("SELECT COUNT(*) as count FROM materials").fetchone()['count'],
        'orders_count': db.execute("SELECT COUNT(*) as count FROM orders").fetchone()['count'],
        'orders_draft': db.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'draft'").fetchone()['count'],
        'orders_production': db.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'production'").fetchone()['count'],
    }
    
    return jsonify(stats)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    init_db()
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False') == 'True'
    
    print("Starting WILD ERP Backend...")
    print(f"Server running on port {port}")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
