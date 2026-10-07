from typing import Literal

from pydantic import BaseModel, Field


class OrderDecision(BaseModel):
    decision: Literal["approve", "flag_for_review"]
    risk_level: Literal["low", "medium", "high"]
    flags: list[str] = Field(default_factory=list)
    reason: str
    recommendation: str


class ReviewDecision(BaseModel):
    decision: Literal["auto_publish", "flag_for_review"]
    toxicity_level: Literal["none", "low", "medium", "high"]
    category: Literal[
        "positive",
        "negative_respectful",
        "negative_offensive",
        "spam",
        "irrelevant",
        "inappropriate",
    ]
    reason: str
