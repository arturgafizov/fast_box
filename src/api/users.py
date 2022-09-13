from typing import Optional, List
from fastapi import FastAPI
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.users import get_user, get_user_by_email, create_user, get_users
from api.utils.courses import get_user_courses
from db.db_setup import get_db, get_async_db
from db.models.user import users
from db.models.course import courses
from schemas.user import UserCreate, User
from schemas.course import Course
from db.db_setup import database

router = fastapi.APIRouter()


# @router.get("/users", response_model=List[User])  # sync
# async def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
#     users = get_users(db, skip=skip, limit=limit)
#     return users


@router.get("/users")
async def read_users():
    query = users.select()
    await database.connect()
    return await database.fetch_all(query)


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with such email already exists")
    return create_user(db=db, user=user)


# @router.get("/users/{user_id}")              #sync
# async def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user(db=db, user_id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User is not found")


@router.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User is not found")
    return user


# @router.get("/users/{user_id}/courses", response_model=List[Course])  # sync
# async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
#     courses = get_user_courses(user_id=user_id, db=db)
#     return courses


@router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(user_id: int,):
    query = courses.select().filter(user_id == user_id)
    await database.connect()
    return await database.fetch_all(query)

