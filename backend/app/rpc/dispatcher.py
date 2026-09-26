from pydantic import ValidationError

from app.rpc.registry import registry


async def dispatch(method: str, params: dict):
    rpc_method = registry.get(method)

    if rpc_method is None:
        return None, {
            "code": -32601,
            "message": "Method not found",
        }

    try:
        data = rpc_method.data_model.model_validate(params)
    except ValidationError as exc:
        return None, {
            "code": -32602,
            "message": "Invalid params",
            "data": exc.errors(),
        }

    try:
        result = await rpc_method.handler(data)
    except Exception:
        return None, {
            "code": -32603,
            "message": "Internal error",
        }

    return result, None