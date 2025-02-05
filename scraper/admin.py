from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('rating', 'created_at')