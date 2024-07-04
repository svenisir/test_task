from fastapi import Query

from app.memes.schemas import SPagination


def pagination_params(
        page: int = Query(ge=1, required=False, default=1, le=100_000),
        per_page: int = Query(ge=1, le=100, required=False, default=10),
):
    return SPagination(page=page, per_page=per_page)
