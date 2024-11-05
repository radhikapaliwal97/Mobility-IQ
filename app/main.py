"""
This module initializes the FastAPI app, handles dependencies, and defines the API routes.
"""

from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mobility CRUD API", swagger_ui_parameters={"syntaxHighlight": False}
)


@app.post("/users", response_model=schemas.User, status_code=201)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """
    Create a new user in the database.
    """
    db_user = models.User(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        date_of_birth=user.date_of_birth,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)) -> List[schemas.User]:
    """
    Retrieve all users from the database.
    """
    users = db.query(models.User).all()
    return users
