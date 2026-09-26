from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AddTea(BaseModel):
    name: str = Field(description="Название чая")
    price: Decimal = Field(description="Цена чая")
    description: str | None = Field(default=None, description="Описание чая")


class EditTea(BaseModel):
    id: int = Field(description="Идентификатор чая")
    name: str | None = Field(default=None, description="Название чая")
    price: Decimal | None = Field(default=None, description="Цена чая")
    description: str | None = Field(default=None, description="Описание чая")


class OutTea(BaseModel):
    id: int = Field(description="Идентификатор чая")
    name: str = Field(description="Название чая")
    price: Decimal = Field(description="Цена чая")
    description: str | None = Field(default=None, description="Описание чая")

    model_config = ConfigDict(from_attributes=True)


class ListTea(BaseModel):
    items: list[OutTea] = Field(description="Список чаёв")