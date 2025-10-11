from flask import Blueprint, jsonify
from app.database.connection import engine
from sqlalchemy import text

# Creamos el Blueprint
routes = Blueprint('routes', __name__)

# Ruta simple de prueba
@routes.route('/ping')
def ping():
    return jsonify({"message": "🏓 Pong! El servidor Flask está activo."})

# Ruta para listar usuarios del sistema
@routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM UsuarioSistema"))
            usuarios = [
                dict(row._mapping) for row in result
            ]
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
