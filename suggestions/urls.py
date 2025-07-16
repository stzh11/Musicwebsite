from django.urls import path

from .views import suggest_song_edit, moderate_song_edits



urlpatterns = [
    # … ваши остальные урлы …
    path(
        "song/<slug:slug>/suggest-edit/",
        suggest_song_edit,
        name="song-suggest-edit"
    ),
    path(
        "moderation/song-edits/",
        moderate_song_edits,
        name="moderate-song-edits"
    ),
]
