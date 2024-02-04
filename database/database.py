import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Для Docker настроек Server должен быть имя контейнера
DATABASE_URL = f"postgresql://{os.getenv('USER')}:{os.getenv('PASSWORD')}\
@{os.getenv('SERVER')}:5432/{os.getenv('DB')}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
