from flask import Flask
from app.database.connection import engine
from app.routes.routes import routes  
from sqlalchemy import text
from app.routes.clientes_routes import clientes_routes
from app.routes.usuarios_route import usuarios_routes
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Registrar las rutas del Blueprint
app.register_blueprint(routes)  # 👈 REGISTRO CORRECTO DEL BLUEPRINT
app.register_blueprint(clientes_routes)
app.register_blueprint(usuarios_routes)

@app.route('/')
def home():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "Conexión a la base de datos exitosa desde Flask"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

