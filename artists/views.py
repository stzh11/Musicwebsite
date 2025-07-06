# artists/views.py
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from .models import Artist, ArtistClaimed, ArtistLink, Subscription
from music.models import SongConnection
from django.shortcuts import redirect

def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)

    conns = (
        SongConnection.objects
        .filter(artist=artist)
        .select_related("song")
    )
    subscribers = Subscription.objects.filter(artist=artist, is_active=True)
    subscribers = subscribers.select_related("subscriber") 
    users = [sub.subscriber for sub in subscribers ]
    print(users)
    songs_roles = {}
    for conn in conns:
        song = conn.song
        songs_roles.setdefault(song, []).append(conn.get_role_display())
    print(songs_roles)
    return render(request, "artists/artist_detail.html", {
        "artist": artist,
        "songs_roles": songs_roles,
        "subscribers": {
            "count": subscribers.count(),
            "users": users,
        },
    })


def subscribe_toggle(request, slug):
    artist = get_object_or_404(Artist, slug=slug)

    qs = Subscription.objects.filter(
        subscriber=request.user,
        artist=artist
    )

    if qs.exists():
        # Получаем сам объект подписки
        subscription = qs.first()

        # Переключаем флаг is_active
        subscription.is_active = not subscription.is_active
        subscription.save()
    
    else:
        # Если подписки ещё не было — создаём новую
        Subscription.objects.create(
            subscriber=request.user,
            artist=artist,
            is_active=True
        )

    return redirect(artist.get_absolute_url())
