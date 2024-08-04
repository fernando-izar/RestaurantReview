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

def scrape_reviews(restaurant_name: str) -> List[RestaurantReview]:
    url = f"https://www.justeat.it/restaurants-{restaurant_name}/reviews"

    # ChromeDriver Configuration
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vEI0Do"))
        )
        except:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-reviews-items"))
        )
        if not (driver.find_elements(By.CLASS_NAME, "c-reviews-items") or driver.find_elements(By.CLASS_NAME, "vEI0Do")):
            return []
        
        page_source = driver.page_source
    finally:
        driver.quit()

    # Gravar o conteúdo de page_source em um arquivo externo (debug)
    # with open('page_source.html', 'w', encoding='utf-8') as file:
    #     file.write(page_source)

    # Option 2: Using requests
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }

    # try:
    #     response = requests.get(url, headers=headers)
    #     response.raise_for_status()  
    # except requests.exceptions.RequestException as e:
    #     raise Exception(f"Failed to fetch reviews for {restaurant_name}: {e}")
    

    soup = BeautifulSoup(page_source, "html.parser")
    reviews = []

    template_type = get_type_of_review(soup)

    review_elements = get_review_elements(soup, template_type)
    
    for element in review_elements:
        # Extract reviewer
        reviewer = get_reviewer(element, template_type)
        reviewer_element = element.find('div', class_='_1AzTo')
        
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