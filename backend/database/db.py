"""
Database connection and session management.

This module handles SQLite database connection setup and session creation
for the Code Craze application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Create database directory if it doesn't exist
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)

# Database URL - SQLite for simplicity
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_DIR}/code_craze.db")

# Create engine
# Reason: check_same_thread=False is needed for SQLite to work with FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Get database session for dependency injection.

    Yields:
        Session: SQLAlchemy database session.

    Example:
        @app.get("/users/")
        def read_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.

    This should be called once at application startup.
    """
    from backend.database.models import User, UserCompetency, QuestionAttempt, UserPreference, Question, Badge, UserBadge, Progress

    Base.metadata.create_all(bind=engine)
