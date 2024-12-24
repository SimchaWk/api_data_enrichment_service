from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid


class TerrorEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_date: datetime
    country: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    data_source: str = "NewsAPI"
    num_killed: Optional[float] = None
    num_wounded: Optional[float] = None
    attack_type: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @classmethod
    @field_validator("latitude", "longitude")
    def validate_coordinates(cls, value, field):
        if value is not None and not (-180 <= value <= 180):
            raise ValueError(f"{field.name} must be between -180 and 180")
        return value

    @classmethod
    @field_validator("event_date")
    def validate_date(cls, value):
        if value > datetime.now():
            raise ValueError("The event date cannot be in the future")
        return value
