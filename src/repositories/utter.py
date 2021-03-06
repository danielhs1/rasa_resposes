import random
from itertools import islice

import ujson
from sqlalchemy import or_, and_

from src.database.connection import database
from src.database.models.utters import utters
from src.database.utils import get_defaults
from src.schemas.utterance import UtteranceModel, UtteranceCreatedModel, UtterancePredict, UtteranceResponses


async def save(utter: UtteranceModel) -> UtteranceCreatedModel:
    defaults = get_defaults(utters)

    defaults["template"] = utter.template
    defaults["channel"] = utter.channel if utter.channel else defaults["channel"]
    defaults["responses"] = ujson.dumps({
        "text": utter.text,
        "buttons": utter.buttons,
        "image": utter.image,
        "elements": utter.elements,
        "attachments": utter.attachments,
        "custom": utter.custom
    })
    stmt = utters.insert().values(defaults)
    await database.execute(stmt)
    return _prepare_created_utterance(defaults)


async def bulk_save(yaml_responses: dict) -> bool:
    for item in _chunks(yaml_responses):
        bulk_list = []
        for utter_name, values in item.items():
            defaults = get_defaults(utters)
            defaults["template"] = utter_name

            text = []
            buttons = []
            image = None
            elements = []
            attachments = []
            custom = {}
            for sub in values:
                if sub.get('text'):
                    text.append(sub.get('text'))
                if sub.get('buttons'):
                    buttons.append(sub.get('buttons'))
                if sub.get('image'):
                    image = sub.get('image')
                if sub.get('elements'):
                    elements.append(sub.get('elements'))
                if sub.get('attachments'):
                    attachments.append(sub.get('attachments'))
                if sub.get('custom'):
                    custom = sub.get('custom')

            defaults["responses"] = ujson.dumps({
                "text": text,
                "buttons": buttons,
                "image": image,
                "elements": elements,
                "attachments": attachments,
                "custom": custom
            })

            bulk_list.append(defaults)

        stmt = utters.insert().values(bulk_list)
        await database.execute(stmt)

    return True


async def get_utters(utter: UtterancePredict):
    query = utters.select().where(and_(
        utters.c.template == utter.template,
        or_(utters.c.channel == utter.channel.name, utters.c.channel == "any")
    ))
    response = await database.fetch_all(query)

    result = _prepare_get_response(response)
    return result


def _prepare_created_utterance(utterance_dict) -> UtteranceCreatedModel:
    utterance_dict["id"] = str(utterance_dict["id"])
    utterance_dict["created_at"] = utterance_dict["created_at"].isoformat()
    utterance_dict["updated_at"] = utterance_dict["updated_at"].isoformat()
    utterance_dict["responses"] = ujson.loads(utterance_dict["responses"])
    return UtteranceCreatedModel(**utterance_dict)


def _chunks(data, size=100):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}


def _prepare_get_response(response):
    data = {
        "text": [],
        "buttons": [],
        "image": None,
        "elements": [],
        "attachments": [],
        "custom": {}
    }
    for item in response:
        responses = ujson.loads(item.get("responses"))
        for key, value in responses.items():
            if key in ["image", "custom"]:
                data[key] = value
            else:
                data[key] += value

    if len(data["text"]) == 0:
        data["text"] = None
    else:
        data["text"] = random.choice(data["text"])

    return UtteranceResponses(**data)
