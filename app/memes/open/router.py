from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.memes.dao import MemDAO
from app.memes.dependencies import pagination_params
from app.memes.schemas import SPagination, SMem
from app.exceptions import MemNotExist

router = APIRouter(
    prefix="/memes",
    tags=["Получение мемов"]
)


@router.get("")
@cache(expire=30)
async def get_memes(
        pagination: Annotated[SPagination, Depends(pagination_params)],
):
    memes = await MemDAO.get_all(pagination=pagination)
    return memes


@router.get("/{mem_id}")
@cache(expire=30)
async def get_memes_by_id(mem_id: int) -> SMem:
    mem = await MemDAO.get_by_id(mem_id) 
    if not mem:
        raise MemNotExist
    return mem
