from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import get_settings

settings = get_settings()

# Create a SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import ORM models to ensure they are registered with Base
from infrastructure.database.models import OXTMetricORM, OXTProviderORM

def create_db_and_tables():
    Base.metadata.create_all(engine)