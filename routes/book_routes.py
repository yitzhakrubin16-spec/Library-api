from fastapi import APIRouter, HTTPException

from schemas import CreateBook, UpdateBook

from database.db_connection import DBManager
from database.book_db import BookDB
from database.member_db import MemberDB


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

db = DBManager()
book_repository = BookDB(db)
member_repository = MemberDB(db)

@router.get("")
def get_all():
    return book_repository.get_all_books()

@router.get("/{id}")
def get_by_id(id: int):
    book =  book_repository.get_book_by_id(id)
    if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("")
def create_book(book: CreateBook):
    book_repository.create_book(book)

    return {
        "message": "Book created successfully"
    }

@router.patch("/{id}")
def update_book(id: int, book: UpdateBook):
    existing_book = book_repository.get_book_by_id(id)

    if existing_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    updated = book_repository.update_book(id, book)

    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    return {
        "message": "Book updated successfully"
    }

@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    book = book_repository.get_book_by_id(id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    member = member_repository.get_member_by_id(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if not book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail="Book is not available"
        )

    if not member["is_active"]:
        raise HTTPException(
            status_code=400,
            detail="Member is not active"
        )

    active_borrows = (
        book_repository.count_active_borrows_by_member(member_id)
    )

    if active_borrows >= 3:
        raise HTTPException(
            status_code=400,
            detail="Member has reached maximum borrows"
        )

    book_repository.set_available(
        id=id,
        val=False,
        member_id=member_id
    )

    member_repository.increment_borrows(member_id)

    return {
        "message": f"Book {id} borrowed by member {member_id}"
    }

@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    book = book_repository.get_book_by_id(id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    member = member_repository.get_member_by_id(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if book["is_available"]:
        raise HTTPException(
            status_code=400,
            detail="Book is not borrowed"
        )

    if book["borrowed_by_member_id"] != member_id:
        raise HTTPException(
            status_code=400,
            detail="Book is not borrowed by this member"
        )

    book_repository.set_available(
        id=id,
        val=True,
        member_id=member_id
    )

    return {
        "message": f"Book {id} returned by member {member_id}"
    }