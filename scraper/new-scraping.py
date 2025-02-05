from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from django.utils import timezone
from .models import Product
import random

def scrape_takealot_products(search_url=None):
    base_url = 'https://www.takealot.com'
    search_url = search_url or urljoin(base_url, '/all?filter=Popularity%20Descending')

    session = requests.Session()
    session.headers.update(HEADERS)

    # Updated headers to mimic a real browser
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'DNT': '1',  # Do Not Track
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        print(f"Fetching URL: {search_url}")
        response = session.get(search_url)
        print(f"Status Code: {response.status_code}")
        response.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')

    # Updated selector for 2024
    products = soup.select('div[data-product-position]')
    print(f"Found {len(products)} products using updated selector")

    for product in products:
        try:
            name = product.select_one('h3.product-title').text.strip()
            price = product.select_one('div.price').text.strip().replace('R', '').replace(',', '')
            rating_element = product.select_one('div.rating')
            rating = float(rating_element.text.strip()) if rating_element else None
            url = urljoin(base_url, product.select_one('a.product-anchor')['href'])

            # Save the product
            Product.objects.update_or_create(
                url=url,
                defaults={
                    'name': name,
                    'price': float(price),
                    'rating': rating,
                    'description': '',  # You can scrape this from the product page if needed
                    'created_at': timezone.now()
                }
            )
            print(f"Saved product: {name}")
        except Exception as e:
            print(f"Error processing product: {e}")