from django.urls import path
from .views import artist_detail

app_name = "artists"

urlpatterns = [
    path("<slug:slug>/", artist_detail, name="artist-detail"),
]