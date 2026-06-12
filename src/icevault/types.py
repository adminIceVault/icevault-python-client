from decimal import Decimal
import typing
from pydantic import BaseModel, Field, PlainSerializer
from uuid import UUID

DecimalStr = typing.Annotated[
    Decimal,
    PlainSerializer(lambda v: str(v), return_type=str)
]
UUIDStr = typing.Annotated[
    UUID,
    PlainSerializer(lambda v: str(v), return_type=str)
]