# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.testing.suite.test_reflection import users
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
#from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(
    prefix="/users",
    tags=["users"],
    #responses={404: {"description": "Not found"}},
)

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    #users = db.scalar(select(User).where(User).all())
    return users

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user =db.execute(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User wasnot found")
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], user: CreateUser):
    db.execute(insert(User).values(username=user.username, firstname=user.firstname, lastname=user.lastname,
                                   age=user.age, slug=slugify(user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successfully'
    }

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, UpdateUser:CreateUser):
    user = db.execute(select(User).where(User.id == user_id))
    print(f'user: {user}')
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User was not found"
        )
    db.execute(update(User).where(User.id == user_id).values(
        username=UpdateUser.username, firstname=UpdateUser.firstname,
        lastname=UpdateUser.lastname, age=UpdateUser.age,
        slug=slugify(UpdateUser.username)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User updated successfully'
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.execute(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted successfully'
    }



