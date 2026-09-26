from sqlalchemy import select

from app.db.connection import async_session_factory
from app.models import InId, InFilter
from app.modules.models.tea import AddTea, EditTea, ListTea, OutTea
from app.modules.orm.tea import Tea
from app.rpc.registry import rpc


@rpc("tea.add")
async def add(data: AddTea) -> OutTea:
    async with async_session_factory() as session:
        tea = Tea(**data.model_dump())
        session.add(tea)
        await session.commit()
        await session.refresh(tea)
        return OutTea.model_validate(tea)


@rpc("tea.edit")
async def edit(data: EditTea) -> OutTea | None:
    async with async_session_factory() as session:
        tea = await session.get(Tea, data.id)
        if tea is None:
            raise ValueError("Tea not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            if field != "id":
                setattr(tea, field, value)

        await session.commit()
        await session.refresh(tea)

        return OutTea.model_validate(tea)

@rpc("tea.get")
async def get(data: InId) -> OutTea:
    async with async_session_factory() as session:
        tea = await session.get(Tea, data.id)
        if tea is None:
            raise ValueError("Tea not found")
        return OutTea.model_validate(tea)


@rpc("tea.list")
async def list(data: InFilter) -> ListTea:
    async with async_session_factory() as session:
        result = await session.execute(select(Tea).offset(data.offset).limit(data.limit))
        teas = result.scalars().all()
        return ListTea(items=[OutTea.model_validate(tea) for tea in teas])