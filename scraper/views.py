from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .scraping import scrape_takealot_products

def home(request):
    return render(request, 'home.html')

def scrape_products(request):
    if request.method == 'POST':
        try:
            scrape_takealot_products()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return render(request, 'scrape.html')

def scrape_complete(request):
    return render(request, 'scrape_complete.html')

def scrape_error(request):
    error = request.GET.get('error', "An unspecified error occurred.")
    return render(request, 'scrape_error.html', {'error': error})