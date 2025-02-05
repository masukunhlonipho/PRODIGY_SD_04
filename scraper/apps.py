from django.apps import AppConfig


class ScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraper'
    label = 'scraper'  # Adding a unique label to avoid conflicts ... this is wrong