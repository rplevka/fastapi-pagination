from __future__ import annotations

from typing import Optional, TypeVar

from sqlalchemy.orm import Query
from sqlalchemy.sql import Select

from ..api import create_page, resolve_params
from ..bases import AbstractPage, AbstractParams

T = TypeVar("T", Select, Query)


def paginate_query(query: T, params: AbstractParams) -> T:
    params = params.to_limit_offset()
    return query.limit(params.limit).offset(params.offset)  # type: ignore


def paginate(query: Query, params: Optional[AbstractParams] = None) -> AbstractPage:
    params = resolve_params(params)

    total = query.count()
    items = paginate_query(query, params).all()

    return create_page(items, total, params)


__all__ = ["paginate_query", "paginate"]
