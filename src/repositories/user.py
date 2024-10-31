from src.repositories.sqlalchemy import SQLAlchemyRepository
from src.models.user import User



class UserRepository(SQLAlchemyRepository):

    model: User = User