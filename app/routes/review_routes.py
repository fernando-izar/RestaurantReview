from fastapi import APIRouter, HTTPException
from typing import List
from app.models import RestaurantReview
from app.services.scraper import scrape_reviews
from app.utils.excel_reader import read_reviews_from_excel
import os

router = APIRouter()

reviews: List[RestaurantReview] = []

@router.post("/review", response_model=RestaurantReview)
def add_review(review: RestaurantReview):
    reviews.append(review)
    return review

@router.get("/reviews", response_model=List[RestaurantReview])
def fetch_reviews():
    return reviews

@router.get("/scrape_reviews/", response_model=List[RestaurantReview])
def scrape_reviews_endpoint(restaurant_name: str):
    scraped_reviews = scrape_reviews(restaurant_name)
    reviews.extend(scraped_reviews)
    return scraped_reviews

@router.post("/load_reviews_from_excel/", response_model=List[RestaurantReview])
def load_reviews_from_excel(file_name: str):
    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    excel_reviews = read_reviews_from_excel(file_path)
    reviews.extend(excel_reviews)
    return excel_reviews