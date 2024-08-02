from fastapi import APIRouter, HTTPException
from typing import List
from app.models import RestaurantReview

router = APIRouter()

reviews: List[RestaurantReview] = []

@router.post("/review", response_model=RestaurantReview)
def add_review(review: RestaurantReview):
    reviews.append(review)
    return review

@router.get("/reviews", response_model=List[RestaurantReview])
def fetch_reviews():
    return reviews