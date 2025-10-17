from flask import Blueprint, request, jsonify
from app.database.connection import engine
from sqlalchemy import text

usuarios_routes = Blueprint('usuarios_routes', __name__)

# 🟢 Obtener todos los usuarios
@usuarios_routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM UsuarioSistema"))
            usuarios = [dict(row._mapping) for row in result]
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Obtener un usuario por ID
@usuarios_routes.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM UsuarioSistema WHERE id_usuario = :id"),
                {"id": id_usuario}
            )
            usuario = result.fetchone()
            if usuario:
                return jsonify(dict(usuario._mapping))
            else:
                return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Crear un nuevo usuario
@usuarios_routes.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    INSERT INTO UsuarioSistema (nombre, email, telefono, rol, especialidad)
                    VALUES (:nombre, :email, :telefono, :rol, :especialidad)
                """),
                data
            )
            conn.commit()
        return jsonify({"message": "Usuario creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Actualizar usuario
@usuarios_routes.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_usuario(id_usuario):
    data = request.get_json()
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    UPDATE UsuarioSistema
                    SET nombre = :nombre,
                        email = :email,
                        telefono = :telefono,
                        rol = :rol,
                        especialidad = :especialidad
                    WHERE id_usuario = :id
                """),
                {**data, "id": id_usuario}
            )
            conn.commit()
        if result.rowcount > 0:
            return jsonify({"message": "Usuario actualizado correctamente"})
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟢 Eliminar usuario
@usuarios_routes.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("DELETE FROM UsuarioSistema WHERE id_usuario = :id"),
                {"id": id_usuario}
            )
            conn.commit()
        if result.rowcount > 0:
            return jsonify({"message": "Usuario eliminado correctamente"})
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
