from flask import Flask, jsonify, request
from models import db, Employee
import sqlite3
from utils import count_transactions_this_month

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

def get_db_connection():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "products.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/init", methods=["GET"])
def init_db():
    conn = get_db_connection()
    conn.execute("""
                CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
                )
                """
                )
    conn.commit()
    conn.close()
    return jsonify({"message": "Database init complete"})

@app.route("/") 
def home():
    return jsonify({"message": "Hello from team Ballest Balls!"})

@app.route("/products", methods=["GET"]) #Получить данные без изменений
def get_products():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

#В целом не нужно именно для продуктов, ибо у нас один вид, но вписал это просто для того чтобы понять и изучить
@app.route("/products", methods=["POST"]) #создать новые данные
def add_products():
    data = request.get_json()
    name = data.get("name")
    conn = get_db_connection()
    cursor = conn.cursor()
    if isinstance(name, str) and name.strip():
        cursor.execute("INSERT INTO products (name) VALUES (?)", (name,))
        conn.commit()
        new_id = cursor.lastrowid
        new_products = {
                "id": new_id,
                "name": name
            }
        conn.close()
        return jsonify({"message": "Product added", "product": new_products}), 201 
    else:
        conn.close()
        return jsonify({"message": "Error 400"}), 400

if __name__ == "__main__":
    with app.app_context():
        init_db()
        db.create_all()
    app.run(debug=True) #В проде залупа, в тесте ахуенчик Илюха соси хуй    