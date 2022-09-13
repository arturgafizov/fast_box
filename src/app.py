from fastapi import FastAPI

from api import sections, courses, users
from db.models import course, user
from db.db_setup import engine

user.Base.metadata.create_all(bind=engine) # можно сделать миграцию без create_all
course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API Test",
    description=" Тестовый сервис для обучения на фаст апи",
    version="0.0.1",
)

app.include_router(users.router)
app.include_router(sections.router)
app.include_router(courses.router)
