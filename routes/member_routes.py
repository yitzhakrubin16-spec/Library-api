from fastapi import APIRouter, HTTPException
from schemas import CreateMember, UpdateMember
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
    member = member_repository.get_member_by_id(id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member

@router.post("")
def create_member(member: CreateMember):
    existing_member = member_repository.get_member_by_email(
        member.email
    )

    if existing_member is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    member_repository.create_member(member)

    return {
        "message": "Member created successfully"
    }


@router.patch("/{id}")
def update_member(id: int, member: UpdateMember):
    existing_member = member_repository.get_member_by_id(id)

    if existing_member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if member.email is not None:
        member_with_email = member_repository.get_member_by_email(member.email)

        if (member_with_email is not None
            and member_with_email["id"] != id):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    updated = member_repository.update_member(id, member)

    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    return {
        "message": "Member updated successfully"
    }


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    member = member_repository.get_member_by_id(id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member_repository.deactivate_member(id)

    return {
        "message": "Member deactivated successfully"
    }

@router.patch("/{id}/activate")
def activate_member(id: int):
    member = member_repository.get_member_by_id(id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    member_repository.activate_member(id)

    return {
        "message": "Member activated successfully"
    }
