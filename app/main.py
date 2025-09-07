from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routes import users, tasks


app = FastAPI(title="ToDo API", version="1.0.0")

#создвем таблицу ри старте (для простоты учебного проекта)
Base.metadata.creat_all(bind=engine)

#подключаем роутеры
app.include_router(user.router)
app.include_router(task.router)

@app.get("/". tags=["health"])
def healthcheck():
    return{"status": "ok"}