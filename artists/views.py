# artists/views.py
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from .models import Artist
from music.models import SongConnection

def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)

    # все связи, где участвует наш артист
    conns = (
        SongConnection.objects
        .filter(artist=artist)
        .select_related("song")
    )

    # группируем по песням, сохраняя порядок добавления
    songs_roles = OrderedDict()
    for conn in conns:
        song = conn.song
        songs_roles.setdefault(song, []).append(conn.get_role_display())
    print(songs_roles)
    return render(request, "artists/artist_detail.html", {
        "artist": artist,
        "songs_roles": songs_roles,   # { song1: ["Вокал","Автор"], song2: [...] }
    })
