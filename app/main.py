"""
This module initializes the FastAPI app, handles dependencies, and defines the API routes.
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, Path
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


@app.delete("/users/{user_id}", response_model=dict)
def delete_user(
    user_id: int = Path(..., description="ID of the user to delete", ge=1),
    db: Session = Depends(get_db),
) -> dict:
    """
    Delete a user from the database by ID.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    db.delete(user)
    db.commit()
    return {"detail": f"User with id {user_id} deleted"}
