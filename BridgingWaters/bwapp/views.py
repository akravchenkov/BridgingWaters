from django.shortcuts import render
from bwapp.models import NewsUpdate

def index(request):
    latest_news_list = NewsUpdate.objects.all().order_by('-created')[:5]
    return render(request, 'bwapp/index.html', {
        'lastest_news_list':latest_news_list
        })