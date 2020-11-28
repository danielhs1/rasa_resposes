from decouple import config

from src import __version__
from src.exceptions.core import ElasticApmUrlIsRequired

APP_PORT = config("APP_PORT", cast=int, default=80)
APP_HOST = config("APP_HOST", default="0.0.0.0")

ENVIRONMENT = config("ENVIRONMENT")
APPLICATION_NAME = config("APPLICATION_NAME")
BASE_PATH = config("BASE_PATH")


ENABLE_MONITORING = config("ENABLE_MONITORING", cast=bool, default=False)
ELASTIC_APM_SERVER_URL = config("ELASTIC_APM_SERVER_URL", default=None)

if ENABLE_MONITORING and not ELASTIC_APM_SERVER_URL:
    raise ElasticApmUrlIsRequired()

ELASTIC_APM = {
    "SERVICE_NAME": f"{ENVIRONMENT}-{APPLICATION_NAME}",
    "SERVICE_VERSION": __version__,
    "COLLECT_LOCAL_VARIABLES": "all",
    "SERVER_URL": ELASTIC_APM_SERVER_URL,
    "CAPTURE_BODY": "all",
}

MASTER_DATABASE = {
    "HOST": config("DB_HOST", default="localhost"),
    "USER": config("DB_USER", default="postgres"),
    "PASSWORD": config("DB_PASSWORD", default="postgres"),
    "NAME": config("DB_NAME"),
}

## IF YOU HAVE A READ DATABASE ONLY SET THE CONFIG HERE
READ_DATABASE = MASTER_DATABASE

MASTER_DATABASE_URL = f"postgresql://{MASTER_DATABASE['USER']}:{MASTER_DATABASE['PASSWORD']}" \
                      f"@{MASTER_DATABASE['HOST']}/{MASTER_DATABASE['NAME']}"

READ_DATABASE_URL = f"postgresql://{READ_DATABASE['USER']}:{READ_DATABASE['PASSWORD']}" \
                      f"@{READ_DATABASE['HOST']}/{READ_DATABASE['NAME']}"
