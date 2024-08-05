# FastAPI Restaurant Reviews Service

This project sets up a FastAPI web service focused on Pydantic validation to manage restaurant reviews. It also includes the option to scrape reviews from JustEat and load reviews from an Excel file.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Pydantic
- Requests
- BeautifulSoup4
- Openpyxl
- Selenium
- Chrome WebDriver

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:fernando-izar/RestaurantReview.git
   cd RestaurantReview
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install the dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application

   ```bash
   uvicorn app.main:app --reload
   ```

2. Available endpoints

- **Add a review:**

  **Method:** `POST`

  **URL:** `/review/`

  **Request body (JSON):**

  ```json
  {
    "data": "2024-08-01",
    "reviewer": "Jane Doe",
    "testo": "Excellent service!",
    "sentiment": 1,
    "voto": 4.5
  }
  ```

- **Retrieve all reviews:**

  **Method:** `GET`

  **URL:** `/reviews/`

- **Scrape reviews:**

  **Method:** `GET`

  **URL:** `/scrape_reviews/`

  **Parameter:** `restaurant_name`

- **Load reviews from an Excel file:**

  **Method:** `POST`

  **URL:** `/load_reviews_from_excel/`

  **Parameter:** `file_name`

  **Note:** Insert the Excel file into the directory `/app/data`
