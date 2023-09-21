from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.main import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=200), nullable=False)