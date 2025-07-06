from django.urls import path
from .views import song_comment_create, album_comment_create

app_name = "comments"

urlpatterns = [
    path(
        "song/<slug:slug>/add/",
        song_comment_create,
        name="song-add-comment"
    ),
    path(
        "album/<slug:slug>/add/",
        album_comment_create,
        name="album-add-comment"
    ),
]