from src.repositories.sqlalchemy import SQLAlchemyRepository
from src.models.item import Item



class ItemRepository(SQLAlchemyRepository):

    model: Item = Item