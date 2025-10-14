from flask import Blueprint, request, jsonify
from app.database.connection import engine
from sqlalchemy import text

clientes_routes = Blueprint('clientes_routes', __name__)

# 🟢 Obtener todos los clientes
@clientes_routes.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM Cliente"))
            clientes = [dict(row._mapping) for row in result]
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Obtener un cliente por ID
@clientes_routes.route('/clientes/<int:id_cliente>', methods=['GET'])
def get_cliente(id_cliente):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM Cliente WHERE id_cliente = :id"),
                {"id": id_cliente}
            )
            cliente = result.fetchone()
            if cliente:
                return jsonify(dict(cliente._mapping))
            else:
                return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Crear un nuevo cliente
@clientes_routes.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO Cliente (nombre, email, telefono, direccion)
                    VALUES (:nombre, :email, :telefono, :direccion)
                """),
                data
            )
            conn.commit()
        return jsonify({"message": "Cliente creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Actualizar cliente existente
@clientes_routes.route('/clientes/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    data = request.get_json()
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    UPDATE Cliente
                    SET nombre = :nombre,
                        email = :email,
                        telefono = :telefono,
                        direccion = :direccion
                    WHERE id_cliente = :id
                """),
                {**data, "id": id_cliente}
            )
            conn.commit()
        if result.rowcount > 0:
            return jsonify({"message": "Cliente actualizado correctamente"})
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Eliminar cliente
@clientes_routes.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("DELETE FROM Cliente WHERE id_cliente = :id"),
                {"id": id_cliente}
            )
            conn.commit()
        if result.rowcount > 0:
            return jsonify({"message": "Cliente eliminado correctamente"})
        else:
            return jsonify({"message": "Cliente no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
