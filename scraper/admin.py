from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'url')  # Fields to show in the admin list view
    search_fields = ('name', 'description')  # Enable search by name and description
