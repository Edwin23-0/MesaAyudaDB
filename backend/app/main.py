from flask import Flask
from app.database.connection import get_connection


app = Flask(__name__)

@app.route('/')
def home():
    try:
        conn = get_connection()
        conn.close()
        return "✅ Conexión a la base de datos exitosa desde Flask"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
