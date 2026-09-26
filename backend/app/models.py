from typing import Any

from pydantic import BaseModel, Field

class InId(BaseModel):
    id: int = Field(description="Идентификатор")


class InFilter(BaseModel):
    limit: int | None = Field(
        default=None,
        description="Ограничение количества записей в одном ответе",
    )
    offset: int | None = Field(
        default=None,
        description="Смещение",
    )
    order: dict[str, Any] | None = Field(
        default=None,
        description="Сортировка",
    )