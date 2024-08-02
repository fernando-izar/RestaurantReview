from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from decimal import Decimal

class RestaurantReview(BaseModel):
    data: date = Field(..., title="Review Date")
    reviewer: str = Field(..., title="Reviewer Name", min_length=1, max_length=100)
    testo: Optional[str] = Field(None, title="Review Text", max_length=1000)
    sentiment: Optional[int] = Field(None, title="Sentiment")
    voto: Decimal = Field(..., title="Rating", ge=0, le=5)

    @field_validator('sentiment')
    def validate_sentiment(cls, sentiment):
        if sentiment not in [None, -1, 0, 1]:
            raise ValueError("Sentiment must be -1, 0, 1 or None")
        return sentiment
    
    @field_validator('voto')
    def validate_voto(cls, voto):
        if voto < 0 or voto > 5:
            raise ValueError("Rating must be between 0 an 5")
        if voto.as_tuple().exponent < -1:
            raise ValueError("Rating must have at most one decimal place")
    
