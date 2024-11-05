"""
This module defines the Pydantic models (schemas) for data validation and serialization.
"""
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """
    Base model for user data validation.
    """

    firstname: str = Field(
        ...,
        max_length=50,
        json_schema_extra={"example": "John"}
    )
    lastname: str = Field(
        ...,
        max_length=50,
        json_schema_extra={"example": "Doe"}
    )
    age: int = Field(
        ...,
        ge=0,
        json_schema_extra={"example": 30}
    )
    date_of_birth: date = Field(
        ...,
        json_schema_extra={"example": "1993-01-01"}
    )


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """


class User(UserBase):
    """
    Schema for a user with ID.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
