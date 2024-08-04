import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from app.models import RestaurantReview
from decimal import Decimal
import ipdb
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locale
from app.utils.italy.functions import get_type_of_review, get_review_elements, get_reviewer, get_review_date, get_review_note, get_review_text, get_review_sentiment
from app.utils.italy.enums import TemplateType

def scrape_reviews(restaurant_name: str) -> List[RestaurantReview]:
    url = f"https://www.justeat.it/restaurants-{restaurant_name}/reviews"
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        try:
            class_name_type1 = TemplateType.TYPE1_REVIEW_CLASS.value
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name_type1))
        )
        except:
            class_name_type2 = TemplateType.TYPE2_REVIEW_CLASS.value
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name_type2))
        )
        if not (driver.find_elements(By.CLASS_NAME, class_name_type1) or driver.find_elements(By.CLASS_NAME, class_name_type2)):
            return []
        
        page_source = driver.page_source
    finally:
        # driver.quit()
        ...

    soup = BeautifulSoup(page_source, "html.parser")
    reviews = []

    # Get the type of review template
    template_type = get_type_of_review(soup)

    # Get the review elements from the page
    review_elements = get_review_elements(soup, template_type)
    
    for element in review_elements:
        # Extract reviewer
        reviewer = get_reviewer(element, template_type)
        
        # Extract date
        review_date = get_review_date(element, template_type)
        
        # Extract review note
        review_note = get_review_note(element, template_type)
        
        # Extract text
        review_text = get_review_text(element, template_type)
       
        # Extract sentiment
        sentiment = get_review_sentiment(element, template_type)
        
        review = RestaurantReview(
            data=review_date,
            reviewer=reviewer,
            testo=review_text,
            sentiment=sentiment,
            voto=review_note
        )
        reviews.append(review)

    return reviews