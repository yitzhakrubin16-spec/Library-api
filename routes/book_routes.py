from fastapi import APIRouter

from database.db_connection import DBManager
from database.book_db import BookDB


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

db = DBManager()
book_repository = BookDB(db)


@router.get("")
def get_all():
    return book_repository.get_all_books()

@router.get("/{id}")
def get_by_id(id: int):
    return book_repository.get_book_by_id(id)

@router.post("")
def create_book(body: dict):
    return book_repository.create_book(body)

@router.patch("/{id}")
def update_book(id:int, body:dict):
    return book_repository.update_book(id, body)

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id:int, member_id: int):
    return book_repository.set_available(id, False, member_id)

@router.patch("/{id}/return/{member_id}")
def return_book(id:int, member_id: int):
    return book_repository.set_available(id, True, member_id)

