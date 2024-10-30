from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger




class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_telegram_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True)