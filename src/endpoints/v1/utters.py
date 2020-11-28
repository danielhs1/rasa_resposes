import random

from fastapi import APIRouter, status, Request

from src.schemas.utterance import UtteranceModel, UtteranceResponse, UtteranceCreatedModel

from src.repositories.utter import save

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


def load_utter_response(utter_response: dict) -> UtteranceResponse:
    return UtteranceResponse(
        text=random.choice(utter_response.get("texts", [])),
        buttons=utter_response.get("buttons", []),
        image=utter_response.get("image"),
        elements=utter_response.get("elements", []),
        attachments=utter_response.get("attachments", []),
        custom=utter_response.get("custom", {})
    )
