from sqlalchemy import select, ChunkedIteratorResult

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).filter_by(**filter_by)
            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).filter_by(**filter_by)
            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns
            ).filter_by(id=model_id)
            result: ChunkedIteratorResult = await session.execute(query)
            return result.mappings().one_or_none() 
