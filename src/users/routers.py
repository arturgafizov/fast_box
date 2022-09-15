from typing import List
import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from users.utils.users import get_user
from db.db_setup import get_async_db
from users.models.user import users
from courses.models.course import courses
from users.schemas.user import UserCreate, User
from courses.schemas.course import Course
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


# @router.post("/users", response_model=User, status_code=201)  # sync
# async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_email(db=db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="User with such email already exists")
#     return create_user(db=db, user=user)


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate):
    query = users.select()
    await database.connect()
    db_user = await database.fetch_one(query.where(users.c.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="User with such email already exists")
    fake_hashed_password = user.password + "not_really_hashed"
    db_user = users.insert().values(email=user.email, role=user.role, password_hash=fake_hashed_password,
                                    is_active=False, created_at=datetime.now(), updated_at=datetime.now())
    user_id = await database.execute(db_user)
    return User(**user.dict(), id=user_id)


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
    query = courses.select()
    await database.connect()
    return await database.fetch_all(query.where(courses.c.user_id == user_id))
