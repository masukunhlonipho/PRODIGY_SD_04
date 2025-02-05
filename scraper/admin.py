from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Product

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    # Write headers
    writer.writerow(['ID', 'Name', 'Price', 'Rating', 'URL', 'Description', 'Created At'])
    
    # Write data
    for obj in queryset:
        writer.writerow([obj.id, obj.name, obj.price, obj.rating, obj.url, obj.description, obj.created_at])
    
    return response

export_to_csv.short_description = "Export selected products to CSV"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('rating', 'created_at')
    actions = [export_to_csv]  # Add the custom action here