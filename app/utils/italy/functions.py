from app.utils.italy.enums import TemplateType
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

def get_type_of_review(soup):  
    if soup.find_all('div', class_='vEI0Do'):
        return TemplateType.TYPE1
    elif soup.find_all('div', class_='c-reviews-item'):
        return TemplateType.TYPE2
    else:
        return TemplateType.UNDEFINED_TYPE

def get_review_elements(soup, template_type):
    if template_type == TemplateType.TYPE1:
        return soup.find_all('div', class_='vEI0Do')
    elif template_type == TemplateType.TYPE2:
        return soup.find_all('div', class_='c-reviews-item')
    else:
        return []
    
def get_reviewer(element, template_type):
    if template_type == TemplateType.TYPE1:
        reviewer_element = element.find('div', class_='_1AzTo')
        return reviewer_element.text.strip()
    elif template_type == TemplateType.TYPE2:
        reviewer_element = element.find('h3', class_='c-reviews-item-reviewer')
        return reviewer_element.text.strip()
    else:  
        return None
    
def get_review_date(element, template_type):
    if template_type == TemplateType.TYPE1:
        date_str_element = element.find('b', class_='Tcels')
        date_str = date_str_element.text.strip()
        return datetime.strptime(date_str, '%A %d %B %Y').date()
    elif template_type == TemplateType.TYPE2:
        date_str_element = element.find('p', class_='c-reviews-item-date')
        date_str = date_str_element.text.strip()
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    else:
        return None
    
def get_review_note(element, template_type):
    if template_type == TemplateType.TYPE1:
        note_div = element.find('div', class_='_15tmo')
        note_title = note_div['title']
        return float(note_title.split(' ')[0])
    elif template_type == TemplateType.TYPE2:
        note_div = element.find('div', class_='RatingMultiStarVariant_c-rating-mask_1c0Q3')
        style = note_div['style']
        percentage = float(style.split('--starRatingPercentage: ')[1].replace('%;', ''))
        return (percentage / 100) * 5
    else:
        return None
    
def get_review_text(element, template_type):
    if template_type == TemplateType.TYPE1:
        testo_element = element.find('b', class_='_3Clmt')
        return testo_element.text if testo_element else None
    elif template_type == TemplateType.TYPE2:
        testo_element = element.find('p', class_='c-review-text')
        return testo_element.text if testo_element else None
    else:
        return
    
def get_review_sentiment(element, template_type):
    if template_type == TemplateType.TYPE1:
        return None
    elif template_type == TemplateType.TYPE2:
        return None
    else:
        return None
    
