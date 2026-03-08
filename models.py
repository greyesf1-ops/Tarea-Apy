from typing import List, Literal
from pydantic import BaseModel, Field


class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORG", "DATE", "LOCATION", "OTHER"]


class ExtractResponse(BaseModel):
    summary: str
    entities: List[Entity]
    actions: List[str]
    confidence: float = Field(..., ge=0, le=1)
    needs_clarification: bool
    clarifying_questions: List[str]


class ExtractRequest(BaseModel):
    text: str
    domain: str
