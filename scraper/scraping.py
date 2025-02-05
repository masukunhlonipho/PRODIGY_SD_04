import time
import os
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from urllib.parse import urljoin
from django.utils import timezone
from .models import Product

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Global HEADERS definition
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

# Global variable to decide whether to use Selenium for scraping
use_selenium = True  # Change this to True if you want to default to using Selenium

def scrape_takealot_products(search_url=None, use_selenium=True, max_scrolls=50):
    base_url = 'https://www.takealot.com'
    search_url = search_url or urljoin(base_url, '/all?filter=Popularity%20Descending')

    if use_selenium:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        options.binary_location = chrome_path
        
        import logging
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(logging.DEBUG)

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(search_url)
            
            # Wait for initial content to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.cell.small-4"))
            )
            
            # Scroll to load more content
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_count = 0

            while scroll_count < max_scrolls:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for new content to load
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    # If height hasn't changed, we've reached the end or no more content to load
                    break
                last_height = new_height
                scroll_count += 1

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Debug: Print the structure of the first product
            products = soup.select('div.cell.small-4')
            if products:
                print("First product element structure:")
                print(products[0].prettify())
            else:
                print("No products found with the selector 'div.cell.small-4'")

        except Exception as e:
            print(f"Selenium error: {e}")
            return
        finally:
            if 'driver' in locals():
                driver.quit()
    else:
        # Non-Selenium logic here if needed
        return

    products = soup.select('div.cell.small-4')
    print(f"Found {len(products)} products")
   
    for product in products:
        product_data = extract_product_data(product, base_url)
        if product_data:
            print(f"Scraped product: {product_data['name']} (Price: {product_data['price']})")
            save_product(product_data)
        else:
            print(f"Failed to extract data for product")
def extract_product_data(product, base_url):
    try:
        # Extract product name
        name_element = product.select_one('h4.product-card-module_product-title_16xh8')
        name = name_element.text.strip() if name_element else 'Unknown Product'

        # Extract product URL
        url_element = product.select_one('a.product-card-module_link-underlay_3sfaA')
        if url_element:
            url = urljoin(base_url, url_element.get('href', ''))
        else:
            print(f"Warning: Could not find URL for product: {name}")
            return None

        # Extract price
        price_element = product.select_one('span.currency.plus.currency-module_currency_29IIm')
        price = float(price_element.text.replace('R', '').strip()) if price_element else 0.0

        # Extract rating
        rating_element = product.select_one('span.score')
        rating = float(rating_element.text.strip()) if rating_element else None

        # Description might not be available in this product card; you might need to fetch from product page
        description = ''  # Placeholder, as description isn't directly in the card

        return {
            'name': name,
            'price': price,
            'url': url,
            'rating': rating,
            'description': description
        }
    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None
def save_product(product_data):
    """Saves product to database, updates if exists"""
    try:
        Product.objects.update_or_create(
            url=product_data['url'],
            defaults={
                'name': product_data['name'],
                'price': product_data['price'],
                'rating': product_data['rating'],
                'description': product_data.get('description', ''),
                'created_at': timezone.now()
            }
        )
    except Exception as e:
        print(f"Error saving product: {e}")