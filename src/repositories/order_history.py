from src.repositories.sqlalchemy import SQLAlchemyRepository
from src.models.order_history import OrderHistory



class OrderHistoryRepository(SQLAlchemyRepository):

    model: OrderHistory = OrderHistory()