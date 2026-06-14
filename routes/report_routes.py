from fastapi import APIRouter

from database.db_connection import DBManager
from database.member_db import MemberDB
from database.book_db import BookDB


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

db = DBManager()
member_repository = MemberDB(db)
book_repository = BookDB(db)

@router.get("/summary")
def get_summary():
    return {
        "total_books": book_repository.count_total_books(),
        "available_books": book_repository.count_available_books(),
        "currently_borrowed": book_repository.count_borrowed_books(),
        "active_members": member_repository.count_active_members()
        }

@router.get("/books-by-genre")
def get_by_genre():
    genres = [{"Genre": "Fiction", "COUNT": 0},
    {"Genre": "Non-Fiction", "COUNT": 0},
    {"Genre": "Science", "COUNT": 0},
    {"Genre": "History", "COUNT": 0},
     {"Genre": "Other", "COUNT": 0}]
    for genre in genres:
        genre["COUNT"] = book_repository.count_by_genre(genre["Genre"])

    return genres
  
@router.get("/top-member")
def get_top_member():
    return member_repository.get_top_member()
