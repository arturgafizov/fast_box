from fastapi import Depends, HTTPException
from typing import Optional, List
import fastapi
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.db_setup import get_db
from api.utils.courses import get_courses, get_course, create_course
from schemas.course import Course, CourseCreate

router = fastapi.APIRouter()


@router.get("/courses", response_model=List[Course])
async def get_read_courses(db: Session = Depends(get_db)):
    course = get_courses(db)
    return course


@router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)


@router.get("/courses/{id}")
async def read_course(course_id: int, db: Session = Depends(get_db)):
    db_user = get_course(db=db, course_id=course_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Course is not found")
    return db_user


@router.patch("/courses/{id}")
async def update_course(id: int):
    return {"courses": []}


@router.delete("/courses/{id}")
async def delete_course(id: int):
    return {"courses": []}
