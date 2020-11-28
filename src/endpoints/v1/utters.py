import random

from fastapi import APIRouter, status, Request

from src.schemas.utterance import UtteranceModel, UtteranceResponse, UtteranceCreatedModel

from src.repositories.utter import save, bulk_save

import yaml

router = APIRouter()


@router.post(
    "/v1/utters",
    tags=["utters"],
    status_code=status.HTTP_201_CREATED,
    summary="Endpoint responsável por criar uma nova utter",
    response_model=UtteranceCreatedModel
)
async def create(utter: UtteranceModel, request: Request):
    return await save(utter)


@router.post(
    "/v1/utters/batch",
    tags=["utters"],
    status_code=status.HTTP_201_CREATED,
    summary="Este endpoint recebe um texto no formato yaml do domain rasa e salva as utters que encontrar no campo response"
)
async def create(request: Request):
    rasa_domain = yaml.safe_load(await request.body())

    responses = rasa_domain.get("responses")
    if responses:
        await bulk_save(responses)
    return None


def load_utter_response(utter_response: dict) -> UtteranceResponse:
    return UtteranceResponse(
        text=random.choice(utter_response.get("texts", [])),
        buttons=utter_response.get("buttons", []),
        image=utter_response.get("image"),
        elements=utter_response.get("elements", []),
        attachments=utter_response.get("attachments", []),
        custom=utter_response.get("custom", {})
    )
