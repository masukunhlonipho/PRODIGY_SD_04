from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
from .models import Product

def scrape_takealot_products():
    url = "https://www.takealot.com/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Update the following logic to target product data
        products = soup.find_all('div', class_='product-card')  # Replace with Takealot's actual class

        for product in products:
            name = product.find('span', class_='product-title').get_text(strip=True)
            price = product.find('span', class_='product-price').get_text(strip=True).replace("R", "")
            rating = product.find('div', class_='star-rating')  # Example, check for existence
            description = product.find('span', class_='product-description').get_text(strip=True)

            Product.objects.create(
                name=name,
                price=float(price),
                rating=float(rating.get('data-rating')) if rating else None,
                url=url,
                description=description
            )
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
