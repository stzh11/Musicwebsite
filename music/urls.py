from django.urls import path
from .views import song_detail, album_detail, song_create
urlpatterns = [
    path("song/create/", song_create, name="song-create"),
    path("song/<slug:slug>/", song_detail, name="song-detail"),
    path("album/<slug:slug>/", album_detail, name="album-detail"),

]
