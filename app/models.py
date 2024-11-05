"""
This module defines the SQLAlchemy models for the application.
"""

from sqlalchemy import Column, Integer, String, Date
from database import Base


class User(Base):
    """
    ORM model for the 'users' table.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def __repr__(self):
        return f"<User(name={self.name}, birth_date={self.birth_date})>"
