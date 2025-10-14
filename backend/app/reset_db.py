# backend/app/reset_db.py
from sqlalchemy.orm import Session
from app.database.connection import engine
from app.models.models import Base

def reset_database():
    print("⚠️  Eliminando todas las tablas y reiniciando IDs...")

    # Elimina todas las tablas
    Base.metadata.drop_all(bind=engine)
    print("🗑️  Tablas eliminadas correctamente.")

    # Crea todas las tablas de nuevo
    Base.metadata.create_all(bind=engine)
    print("🆕  Tablas creadas nuevamente con IDs reiniciados desde 1.")

if __name__ == "__main__":
    reset_database()
