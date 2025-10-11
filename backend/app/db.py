from sqlalchemy.orm import sessionmaker
from app.database.connection import engine

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
