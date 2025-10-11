from flask import Blueprint, request, jsonify
from app.database.connection import engine
from sqlalchemy import text

clientes_routes = Blueprint('clientes_routes', __name__)

# 🔹 Obtener todos los clientes
@clientes_routes.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM Cliente"))
            clientes = [dict(row._mapping) for row in result]
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Crear un nuevo cliente
@clientes_routes.route('/clientes', methods=['POST'])
def add_cliente():
    try:
        data = request.get_json()
        query = text("""
            INSERT INTO Cliente (nombre, email, telefono, direccion)
            VALUES (:nombre, :email, :telefono, :direccion)
        """)
        with engine.begin() as conn:
            conn.execute(query, data)
        return jsonify({"message": "✅ Cliente creado exitosamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Actualizar un cliente
@clientes_routes.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    try:
        data = request.get_json()
        query = text("""
            UPDATE Cliente
            SET nombre = :nombre, email = :email, telefono = :telefono, direccion = :direccion
            WHERE id_cliente = :id
        """)
        with engine.begin() as conn:
            conn.execute(query, {**data, "id": id})
        return jsonify({"message": "✅ Cliente actualizado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Eliminar un cliente
@clientes_routes.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        query = text("DELETE FROM Cliente WHERE id_cliente = :id")
        with engine.begin() as conn:
            conn.execute(query, {"id": id})
        return jsonify({"message": "🗑️ Cliente eliminado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
