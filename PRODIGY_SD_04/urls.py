from django.contrib import admin
from django.urls import path
from scraper import views  # Import all views from scraper app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/', views.scrape_products, name='scrape-products'),  # Updated to function view
    path('', views.home, name='home'),
    path('scrape/complete/', views.scrape_complete, name='scrape-complete'),
]