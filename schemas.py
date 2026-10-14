from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ApplicationStatus = Literal[
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn"
]


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    status: ApplicationStatus


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: ApplicationStatus