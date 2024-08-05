from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import re

class RestaurantReview(BaseModel):
    data: date = Field(..., title="Review Date")
    reviewer: str = Field(..., title="Reviewer Name", min_length=1, max_length=100)
    testo: Optional[str] = Field(None, title="Review Text", max_length=500)
    sentiment: Optional[int] = Field(None, title="Sentiment")
    voto: Decimal = Field(..., title="Rating", ge=0, le=5)

    @field_validator('data')
    def validate_data(cls, data):
        if data > date.today():
            raise ValueError("Review date can't be in the future.")
        return data


    @field_validator('reviewer')
    def validate_reviewer(cls, reviewer):
        reviewer = re.sub(r'[^\w\s]', '', reviewer)
        if len(reviewer) > 100:
            reviewer = reviewer[:100]
        return reviewer

    @field_validator('testo')
    def validate_testo(cls, testo):
        if testo and len(testo) > 500:
            testo = testo[:500]
        return testo

    @field_validator('sentiment')
    def validate_sentiment(cls, sentiment):
        if sentiment not in [None, -1, 0, 1]:
            raise ValueError("Sentiment must be -1, 0, 1 or None")
        return sentiment
    
    @field_validator('voto')
    def validate_voto(cls, voto):
        if voto < 0:
            voto = Decimal(0)
        elif voto > 5:
            voto = Decimal(5)
        voto = voto.quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
        return voto
    
