import uuid
from datetime import datetime
from typing import Optional

from cron_validator import CronValidator
from pydantic import BaseModel, Field, validator


class Weight(BaseModel):
    mass_kg: int
    last_measured: datetime


class MilkProduction(BaseModel):
    last_milk: datetime
    cron_schedule: str
    amount_I: int

    @validator("cron_schedule")
    def validate_cron_schedule(cls, value):
        if CronValidator.parse(value) is not None:
            return value
        raise ValueError("invalid cron schedule expression!")


class Feeding(BaseModel):
    amount_kg: int
    cron_schedule: str
    last_measured: datetime

    @validator("cron_schedule")
    def validate_cron_schedule(cls, value):
        if CronValidator.parse(value) is not None:
            return value
        raise ValueError("invalid cron schedule expression!")


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


class CowModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default_factory=uuid.uuid4)
    name: str
    sex: str
    birthdate: datetime
    condition: str
    weight: Weight
    feeding: Feeding
    milk_production: MilkProduction
    has_calves: bool

    @validator("id")
    def validate_id(cls, value):
        if is_valid_uuid(value):
            return value
        raise ValueError("invalid uuid4!")


class CowUpdate(BaseModel):
    condition: Optional[str] = None
    weight: Optional[Weight] = None
    feeding: Optional[Feeding] = None
    milk_production: Optional[MilkProduction] = None
    has_calves: Optional[str] = None
