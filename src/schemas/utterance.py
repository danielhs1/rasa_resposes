from typing import Optional, List
from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel


class Channel(BaseModel):
    name: str


class Tracker(BaseModel):
    sender_id: str
    slots: Optional[dict]
    latest_message: Optional[dict]
    latest_event_time: Optional[float]
    followup_action: Optional[str]
    paused: Optional[bool]
    events: Optional[list]
    latest_input_channel: Optional[str]
    active_loop: Optional[dict]
    latest_action_name: Optional[str]


class UtterancePredict(BaseModel):
    template: str
    arguments: Optional[dict]
    tracker: Optional[Tracker]
    channel: Channel


class UtteranceResponse(BaseModel):
    text: Optional[str]
    buttons: Optional[str]
    image: Optional[str]
    elements: Optional[str]
    attachments: Optional[str]
    custom: Optional[dict]


class UtteranceModel(BaseModel):
    template: str
    channel: str
    texts: List[str]
    buttons: Optional[List[str]]
    image: Optional[str]
    elements: Optional[List[str]]
    attachments: Optional[List[str]]
    custom: Optional[dict]


class UtteranceResponses(BaseModel):
    texts: Optional[List[str]]
    buttons: Optional[List[str]]
    image: Optional[str]
    elements: Optional[List[str]]
    attachments: Optional[List[str]]
    custom: Optional[dict]


class UtteranceCreatedModel(BaseModel):
    id: str
    template: str
    channel: str
    created_at: str
    updated_at: str
    responses: UtteranceResponses



