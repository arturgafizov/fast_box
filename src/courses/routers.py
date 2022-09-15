from fastapi import Depends, HTTPException
import fastapi
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from db.db_setup import database, get_async_db
from courses.utils.courses import get_course, put_course, get_by_course, delete_course_db
from courses.models.course import courses
from courses.schemas.course import Course, CourseCreate

router = fastapi.APIRouter()


# @router.get("/courses", response_model=List[Course])  # sync
# async def get_read_courses(db: Session = Depends(get_db)):
#     course = get_courses(db)
#     return course


# @router.post("/courses", response_model=Course, status_code=201)  # sync
# async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
#     return create_course(db=db, course=course)


# @router.get("/courses/{id}")  # sync
# async def read_course(course_id: int, db: Session = Depends(get_db)):
#     db_user = get_course(db=db, course_id=course_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="Course is not found")
#     return db_user


@router.get("/courses")
async def get_read_courses():
    query = courses.select()
    await database.connect()
    return await database.fetch_all(query)


@router.post("/courses", response_model=Course, status_code=201)
async def create_new_course(course: CourseCreate):
    await database.connect()
    db_course = courses.insert().values(title=course.title, description=course.description, user_id=course.user_id,
                                        created_at=datetime.now(), updated_at=datetime.now())
    course_id = await database.execute(db_course)
    return Course(**course.dict(), id=course_id)


@router.get("/courses/{course_id}")
async def read_course(course_id: int, db: AsyncSession = Depends(get_async_db)):
    db_course = await get_course(db=db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course is not found")
    return db_course


@router.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: int, course: Course,):
    await database.connect()
    db_course = await get_by_course(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course is not found")
    db_course_id = await put_course(course_id, course)
    response_object = {
        "id": db_course_id,
        "title": course.title,
        "description": course.description,
        "user_id": course.user_id
    }
    return response_object


@router.delete("/courses/{course_id}")
async def delete_course(course_id: int):
    await database.connect()
    db_course = await get_by_course(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course is not found")
    await delete_course_db(course_id)
    return 'Course deleted successfully'
