from itertools import islice

import ujson

from src.database.connection import database
from src.database.models.utters import utters
from src.database.utils import get_defaults
from src.schemas.utterance import UtteranceModel, UtteranceCreatedModel


async def save(utter: UtteranceModel) -> UtteranceCreatedModel:
    defaults = get_defaults(utters)

    defaults["template"] = utter.template
    defaults["channel"] = utter.channel if utter.channel else defaults["channel"]
    defaults["responses"] = ujson.dumps({
        "texts": utter.texts,
        "buttons": utter.buttons,
        "image": utter.image,
        "elements": utter.elements,
        "attachments": utter.attachments,
        "custom": utter.attachments
    })
    stmt = utters.insert().values(defaults)
    await database.execute(stmt)
    return prepare_created_utterance(defaults)


async def bulk_save(yaml_responses: dict) -> bool:
    for item in chunks(yaml_responses):
        bulk_list = []
        for utter_name, values in item.items():
            defaults = get_defaults(utters)
            defaults["template"] = utter_name

            texts = []
            buttons = []
            image = None
            elements = []
            attachments = []
            custom = []
            for sub in values:
                if sub.get('text'):
                    texts.append(sub.get('text'))
                if sub.get('buttons'):
                    buttons.append(sub.get('buttons'))
                if sub.get('image'):
                    image = sub.get('image')
                if sub.get('elements'):
                    elements.append(sub.get('elements'))
                if sub.get('attachments'):
                    attachments.append(sub.get('attachments'))
                if sub.get('custom'):
                    custom.append(sub.get('custom'))

            defaults["responses"] = ujson.dumps({
                "texts": texts,
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


def prepare_created_utterance(utterance_dict) -> UtteranceCreatedModel:
    utterance_dict["id"] = str(utterance_dict["id"])
    utterance_dict["created_at"] = utterance_dict["created_at"].isoformat()
    utterance_dict["updated_at"] = utterance_dict["updated_at"].isoformat()
    utterance_dict["responses"] = ujson.loads(utterance_dict["responses"])
    return UtteranceCreatedModel(**utterance_dict)


def chunks(data, size=100):
    it = iter(data)
    for i in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}


def update():
    pass


def get():
    pass


def delete():
    pass
