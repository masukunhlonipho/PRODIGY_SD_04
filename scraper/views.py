from django.http import HttpResponse, JsonResponse
from django.views import View
from .scraping import scrape_takealot_products

def home(request):
    return HttpResponse("Welcome to the Takealot Scraper! Visit /scrape/ to start scraping.")

class ScrapeProductsView(View):
    def get(self, request):
        try:
            scrape_takealot_products()
            return JsonResponse({'status': 'success', 'message': 'Scraping completed'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)