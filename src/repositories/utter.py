from src.database.models.utters import utters
from src.schemas.utterance import UtteranceModel, UtteranceCreatedModel
from src.database.connection import database
from src.database.utils import get_defaults
import ujson


def save_from_list():
    pass


async def save(utter: UtteranceModel) -> UtteranceCreatedModel:
    defaults = get_defaults(utters)

    defaults["template"] = utter.template
    defaults["channel"] = utter.channel
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


def prepare_created_utterance(utterance_dict) -> UtteranceCreatedModel:
    utterance_dict["id"] = str(utterance_dict["id"])
    utterance_dict["created_at"] = utterance_dict["created_at"].isoformat()
    utterance_dict["updated_at"] = utterance_dict["updated_at"].isoformat()
    utterance_dict["responses"] = ujson.loads(utterance_dict["responses"])
    return UtteranceCreatedModel(**utterance_dict)


def update():
    pass


def get():
    pass


def delete():
    pass
