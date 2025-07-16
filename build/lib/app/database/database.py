from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load DB settings from environment or defaults
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_DATABASE = os.getenv("PG_DATABASE", "vector_db")

DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session local for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to be used in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()