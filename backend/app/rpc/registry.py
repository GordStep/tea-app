import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass
class RpcMethod:
    handler: Callable[[BaseModel], Any]
    data_model: type[BaseModel]


registry: dict[str, RpcMethod] = {}


def rpc(method: str):
    def decorator(func):
        params = list(inspect.signature(func).parameters.values())

        if len(params) != 1 or params[0].name != "data":
            raise TypeError(f"{method}: expected exactly one argument 'data'")

        data_model = params[0].annotation

        if not inspect.isclass(data_model) or not issubclass(data_model, BaseModel):
            raise TypeError(f"{method}: data must be a Pydantic model")

        registry[method] = RpcMethod(
            handler=func,
            data_model=data_model,
        )

        return func

    return decorator