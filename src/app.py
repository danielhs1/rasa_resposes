from uuid import uuid4

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import FastAPI, Request

from src.endpoints import health_check
from src.endpoints.v1 import utters
from src.settings import BASE_PATH, ELASTIC_APM, ENABLE_MONITORING
from src.database.connection import database

app = FastAPI()

if ENABLE_MONITORING:
    app.add_middleware(ElasticAPM, client=make_apm_client(ELASTIC_APM))


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.middleware("http")
async def default_handler(request: Request, call_next):
    request.state.transaction_id = str(uuid4())
    response = await call_next(request)
    return response

app.include_router(
    health_check.router,
    prefix=f"{BASE_PATH}",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    utters.router,
    prefix=f"{BASE_PATH}",
    tags=["utters"],
    responses={404: {"description": "Not found"}},
)
