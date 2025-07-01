from django.shortcuts import render
from .models import News
from django.views.generic import ListView, DetailView

class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    context_object_name = "news_list"
    paginate_by = 10  # Number of news items per page

    def get_queryset(self):
        return News.objects.all().order_by('-created_at')

class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news_item"

    
# Create your views here.
