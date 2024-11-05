"""
This module sets up the database connection and session management using SQLAlchemy.
"""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def get_database_url() -> str:
    """
    Construct and return the database URL from environment variables.

    Returns:
        str: The URL for the database connection.
    """
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not all([db_user, db_password, db_name, db_host, db_port]):
        raise ValueError("Database configuration is incomplete. Please check environment variables.")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = get_database_url()

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, future=True)

# Create a Base class for our ORM models
Base = declarative_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    future=True
)


def get_db() -> Generator:
    """
    Dependency to get a SQLAlchemy session.
    Yields:
        A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
