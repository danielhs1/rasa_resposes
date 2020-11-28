from uuid import uuid4

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import FastAPI, Request

from src.handlers import health_check
from src.settings import BASE_PATH, ELASTIC_APM, ENABLE_MONITORING

app = FastAPI()

if ENABLE_MONITORING:
    app.add_middleware(ElasticAPM, client=make_apm_client(ELASTIC_APM))


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
