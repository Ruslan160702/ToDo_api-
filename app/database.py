from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = 'sqlite:///./todo.db'


engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}, #нужно дял SQLite в одиночном потоке
)

Sessionlocal = sessionmaker(bind-engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy"""
    pass

def get_db() -> Generator:
    """Зависимость FastAPI: выдает сессию БД и коректно закрывает её."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()