import sqlalchemy
from databases import Database

from src.settings import MASTER_DATABASE_URL

database = Database(MASTER_DATABASE_URL)
metadata = sqlalchemy.MetaData()
