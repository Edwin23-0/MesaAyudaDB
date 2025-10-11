from sqlalchemy import create_engine

# Configuración de conexión
server = r"localhost\SQLEXPRESS"
database = "MesaAyudaDB"

# Cadena de conexión con autenticación de Windows
connection_string = f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# Crear el motor global
engine = create_engine(connection_string)

def get_connection():
    """
    Devuelve una conexión activa a la base de datos.
    """
    try:
        conn = engine.connect()
        print("✅ Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print("❌ Error al conectar:", e)
        return None
