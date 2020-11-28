from datetime import datetime
from uuid import uuid4

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from src.database.connection import metadata

utters = sqlalchemy.Table(
    "utters",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        index=True,
        default=uuid4
    ),
    sqlalchemy.Column("template", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("channel", sqlalchemy.String, nullable=False, default="any"),
    sqlalchemy.Column("responses", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
)
