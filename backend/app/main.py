from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from app.db.base import Base
from app.db.connection import engine
from app.modules.controller import tea
from app.rpc.dispatcher import dispatch


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/api")
async def api(request: dict):
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    if not isinstance(method, str):
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request",
            },
            "id": request_id,
        }

    if not isinstance(params, dict):
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32602,
                "message": "Invalid params",
            },
            "id": request_id,
        }

    result, error = await dispatch(method, params)

    if error:
        return {
            "jsonrpc": "2.0",
            "error": error,
            "id": request_id,
        }

    return {
        "jsonrpc": "2.0",
        "result": jsonable_encoder(result),
        "id": request_id,
    }