from fastapi import FastAPI

from users import routers as users_routers
from courses import routers as courses_routers, sections
from users.models import user
from courses.models import course
from db.db_setup import engine

user.Base.metadata.create_all(bind=engine) # можно сделать миграцию без create_all
course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API Test",
    description=" Тестовый сервис для обучения на фаст апи",
    version="0.0.1",
)

app.include_router(users_routers.router)
app.include_router(sections.router)
app.include_router(courses_routers.router)
