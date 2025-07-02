from django.urls import path
from .views import song_detail, album_detail
urlpatterns = [
    path("song/<slug:slug>/", song_detail, name="song-detail"),
    path("album/<slug:slug>/", album_detail, name="album-detail"),
]
