from django.urls import path
from .views import artist_detail, subscribe_toggle

app_name = "artists"

urlpatterns = [
    path("<slug:slug>/", artist_detail, name="artist-detail"),
    path("<slug:slug>/subscribe/", subscribe_toggle, name="subscribe-toggle"),
]