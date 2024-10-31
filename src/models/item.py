from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Sequence, Identity, ARRAY



class Item(Base):
    __tablename__ = 'items'

    article: Mapped[int] = mapped_column(Identity(start=100000, increment=1), primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int] = mapped_column(default=0)
    sizes: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    photo_id: Mapped[str]