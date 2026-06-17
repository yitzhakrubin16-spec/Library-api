from typing import Literal

from pydantic import BaseModel, Field

Genre = Literal[
    "Fiction",
    "Non-Fiction",
    "Science",
    "History",
    "Other"
]



class CreateBook(BaseModel):
    title : str = Field(max_length=50)
    author : str = Field(max_length=50)
    genre : Genre


class UpdateBook(BaseModel):    
    title : str | None  = Field(max_length=50, default=None)
    author : str | None = Field(max_length=50, default=None)
    genre : Genre | None = None


class CreateMember(BaseModel):
    name: str = Field(max_length=50)
    email: str


class UpdateMember(BaseModel):
    name: str | None = Field( max_length=50, default=None)
    email: str | None = None