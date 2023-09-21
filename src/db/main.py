from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from settings import settings

engine = create_async_engine(settings.db_dsn, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(AsyncAttrs, DeclarativeBase):
    pass