from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, BigInteger, DateTime
from sqlalchemy.sql import func


class OrderHistory(Base):
    __tablename__ = 'order_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    order_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
