from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Sequence



class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped[Integer] = mapped_column(Integer, Sequence(name='Article', start=100000, increment=1), unique=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int] = mapped_column(default=0)
    photo_id: Mapped[str]