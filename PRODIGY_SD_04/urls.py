from django.contrib import admin
from django.urls import path
from scraper.views import ScrapeProductsView, home  # Import the home view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/', ScrapeProductsView.as_view(), name='scrape-products'),
    path('', home, name='home'),  # Map root path to the home view
]