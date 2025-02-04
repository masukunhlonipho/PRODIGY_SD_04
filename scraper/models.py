from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True, blank=True)  # Optional
    url = models.URLField(max_length=500)
    description = models.TextField(null=True, blank=True)  # For product specifications or details

    def __str__(self):
        return self.name
