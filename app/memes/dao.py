from __future__ import annotations

from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy import ChunkedIteratorResult, delete, func, insert, select, update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import CannotAddMemException, CannotUpdateMemException, MemNotExist
from app.memes.dependencies import pagination_params
from app.memes.model import Memes
from app.memes.schemas import SPagination


class MemDAO(BaseDAO):
    model = Memes

    @classmethod
    async def get_all(
        cls, pagination: Annotated[SPagination, Depends(pagination_params)]
    ):
        async with async_session_maker() as session:
            query = (
                select(cls.model.__table__.columns)
                .limit(pagination.per_page)
                .offset(
                    pagination.page - 1
                    if pagination.page == 1
                    else (pagination.page - 1) * pagination.per_page
                )
            )

            result: ChunkedIteratorResult = await session.execute(query)

            count_all_rows_query = select(func.count()).select_from(cls.model)
            count_all_rows: ChunkedIteratorResult = await session.execute(
                count_all_rows_query
            )
            count_all_rows = count_all_rows.scalar()

            pagination_result = {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "pages": ceil(count_all_rows / pagination.per_page),
            }

            return result.mappings().all(), pagination_result

    @classmethod
    async def add(cls, description: str, file_name: str):
        async with async_session_maker() as session:
            # query for database
            query = (
                insert(cls.model)
                .values(description=description, file_name=file_name)
                .returning(cls.model.id)
            )

            # execute query and returning id of the added record
            model_id: ChunkedIteratorResult = await session.execute(query)
            model_id = model_id.scalar()

            # checking if the record has been added
            if not model_id:
                raise CannotAddMemException

            # commit in case of successful addition of the record
            await session.commit()

            # returning id of the added record
            return model_id

    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            # query for database
            query = delete(cls.model).filter_by(id=model_id).returning(cls.model)

            # execute query and returning added record
            mem: ChunkedIteratorResult = await session.execute(query)
            mem = mem.scalar()

            # checking if the record has been deleted
            if mem is None:
                raise MemNotExist

            # commit in case of successful deletion of the record
            await session.commit()

            # returning deleted mem
            return mem

    @classmethod
    async def update(
        cls,
        model_id: int,
        file_name: str,
        description: str,
    ):
        async with async_session_maker() as session:
            # query for database to update record with model_id
            query = (
                update(Memes)
                .where(Memes.id == model_id)
                .values(description=description, file_name=file_name)
                .returning(cls.model)
            )

            # execute query and returning record id
            mem = await session.execute(query)
            mem = mem.scalar()

            # checking if the record has been updated
            if mem is None:
                raise CannotUpdateMemException

            # commit in case of successful updating of the record
            await session.commit()

            return mem
