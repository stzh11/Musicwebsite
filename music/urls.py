from django.urls import path
from .views import song_detail, album_detail, song_create, song_like_toggle, album_like_toggle, add_song_annotation


urlpatterns = [
    path( "song/<slug:slug>/add_annotation/", add_song_annotation, name="add_annotation"),
    path("song/create/", song_create, name="song-create"),
    path("song/<slug:slug>/", song_detail, name="song-detail"),
    path("album/<slug:slug>/", album_detail, name="album-detail"),
    path("song/<slug:slug>/like/", song_like_toggle, name="song-like-toggle"),
    path("album/<slug:slug>/like/", album_like_toggle, name="album-like-toggle"),

]
