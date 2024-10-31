from src.repositories.base import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select
from logger import logger
from sqlalchemy.exc import SQLAlchemyError



class SQLAlchemyRepository(AbstractRepository):

    model = None


 
    @classmethod
    async def add(self, session: AsyncSession, **data: dict):
        try:
            stmt = insert(self.model).values(**data).returning(self.model.__table__.columns)
            res = await session.execute(stmt)
            await session.commit()
            return res.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error('Ошибка при добавлении записи в базу данных', extra={'данные': data, 'ошибка': e})
            return None


    @classmethod
    async def find_one_or_none(self, session: AsyncSession, **filter_by):
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при поиске значения в базе данных', extra={'ошибка': e})
            return None


    @classmethod
    async def find_all(self, session: AsyncSession, **filter_by):
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            return res.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при поиске всех значений в базе данных', extra={'ошибка': e})
            return None
            

    @classmethod
    async def delete(self, session: AsyncSession, article: int):
        try:
            stmt = delete(self.model).filter_by(article=article).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f'Ошибка при удалении значения из базы данных', extra={'ошибка': e})
            return None