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

locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

def scrape_reviews(restaurant_name: str) -> List[RestaurantReview]:
    url = f"https://www.justeat.it/restaurants-{restaurant_name}/reviews"

    # ChromeDriver Configuration
    # service = Service(ChromeDriverManager().install())
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
        ...
        driver.quit()

    # Gravar o conteúdo de page_source em um arquivo externo
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
    review_elements = soup.find_all('div', class_='vEI0Do')
    print(len(review_elements))
    if not review_elements:
        review_elements = soup.find_all('div', class_='c-reviews-item') 
    
    for element in review_elements:
        # Extract reviewer
        reviewer_element = element.find('div', class_='_1AzTo')
        if not reviewer_element:
            reviewer_element = element.find('h3', attrs={'data-test-id': 'review-author'})
        reviewer = reviewer_element.text.strip() if reviewer_element else 'Test User'
        
        # Extract date
        date_str_element = element.find('b', class_='Tcels')
        date_str = date_str_element.text.strip() if date_str_element else None
        review_date = datetime.strptime(date_str, '%A %d %B %Y').date() if date_str else None

        if not review_date:
            date_str_element = element.find('p', class_='c-reviews-item-date')
            date_str = date_str_element.text.strip() if date_str_element else None
            review_date = datetime.strptime(date_str, '%d/%m/%Y').date() if date_str else None
        
        # Extract rating
        # rating_div = element.find('div', class_='_15tmo', attrs={'data-qa': 'rating-display-element'})
        # voto_title = rating_div['title']
        # voto = Decimal(voto_title.split(' ')[0])  
        rating_div = element.find('div', class_='_15tmo')
        if rating_div:
            voto_title = rating_div['title']
            voto = float(voto_title.split(' ')[0])

        if not rating_div:
            rating_div = element.find('div', class_='RatingMultiStarVariant_c-rating-mask_1c0Q3')

            if rating_div:
                style = rating_div['style']
                percentage = float(style.split('--starRatingPercentage: ')[1].replace('%;', ''))
                voto = (percentage / 100) * 5
        

        
        # Extract text
        testo_element = element.find('b', class_='_3Clmt')
        if not testo_element:
            testo_element = element.find('p', attrs={'data-test-id': 'review-text'})
        testo = testo_element.text if testo_element else None
        
        # Sentiment is set to None as per requirement
        sentiment = None
        
        review = RestaurantReview(
            data=review_date,
            reviewer=reviewer,
            testo=testo,
            sentiment=sentiment,
            voto=voto
        )
        reviews.append(review)

    return reviews