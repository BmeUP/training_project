from sqlalchemy import Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.main import Base
from src.db.models.user import User


class Card(Base):
    __tablename__ = "users_card"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(Integer(), nullable=False)
    balance: Mapped[str] = mapped_column(DECIMAL(), nullable=False, unique=False)
    pin: Mapped[str] = mapped_column(Integer(), nullable=False, unique=False)
    svv: Mapped[str] = mapped_column(Integer(), nullable=False)
    holder: Mapped[int] = mapped_column(ForeignKey(User.id))