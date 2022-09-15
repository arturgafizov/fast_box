from sqlalchemy.orm import Session
from datetime import datetime
from courses.models.course import Course, courses
from courses.schemas.course import CourseCreate

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import database


# def get_course(db: Session, course_id: int):  # sync
#     return db.query(Course).filter(Course.id == course_id).first()

async def get_course(db: AsyncSession, course_id: int):
    query = select(Course).where(Course.id == course_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_by_course(course_id: int):  # second solution
    query = courses.select().where(course_id == courses.c.id)
    return await database.fetch_one(query)


async def put_course(course_id: int, course: Course):
    query = (
        courses.update().where(course_id == courses.c.id).values(title=course.title, description=course.description,
                                                                 user_id=course.user_id).returning(courses.c.id)
    )
    return await database.execute(query)


async def delete_course_db(course_id: int):
    query = (
        courses.delete().where(course_id == courses.c.id)
    )
    return await database.execute(query)


async def create_course(course: CourseCreate):
    query = courses.insert().values(title=course.title, description=course.description, user_id=course.user_id,
                                        created_at=datetime.now(), updated_at=datetime.now())
    course_id = await database.execute(query)
    return course_id


def get_courses(db: Session):  # sync
    return db.query(Course).all()


def get_user_courses(db: Session, user_id: int):  # sync
    courses = db.query(Course).filter(Course.user_id == user_id).all()
    return courses


# def create_course(db: Session, course: CourseCreate):  # sync
#     db_course = Course(
#         title=course.title,
#         description=course.description,
#         user_id=course.user_id
#     )
#     db.add(db_course)
#     db.commit()
#     db.refresh(db_course)
#     return db_course
