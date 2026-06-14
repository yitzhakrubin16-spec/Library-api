from fastapi import APIRouter

from database.db_connection import DBManager
from database.member_db import MemberDB


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)

db = DBManager()
member_repository = MemberDB(db)


@router.get("")
def get_all():
    return member_repository.get_all_members()

@router.get("/{id}")
def get_by_id(id: int):
    return member_repository.get_member_by_id(id)

@router.post("")
def create_member(body: dict):
    return member_repository.create_member(body)

@router.patch("/{id}")
def update_member(id:int, body:dict):
    return member_repository.update_member(id, body)

@router.patch("/{id}/deactivate")
def deactivate_member(id:int):
    return member_repository.deactivate_member(id)

@router.patch("/{id}/activate")
def activate_member(id: int):
    return member_repository.activate_member(id)

