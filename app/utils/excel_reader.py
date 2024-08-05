import pandas as pd
from typing import List
from app.models import RestaurantReview
from datetime import date, datetime
from decimal import Decimal
import ipdb

def read_reviews_from_excel(file_path: str) -> List[RestaurantReview]:
    df = pd.read_excel(file_path)
    reviews = []

    for _, row in df.iterrows():
        date_value = row['data']
        if not isinstance(date_value, datetime):
            date_value = datetime.strptime(str(date_value), '%Y-%m-%d')
        else: 
            date_value = date_value.date()

        testo = row['testo'] if not pd.isna(row['testo']) else None
        sentiment = row['sentiment'] if not pd.isna(row['sentiment']) else 0

        review = RestaurantReview(
            data=date_value,
            reviewer=row['reviewer'],
            testo=testo,
            sentiment=sentiment,
            voto=Decimal(row['voto'])
        )
        reviews.append(review)
        
    return reviews