from collections import defaultdict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Song, SongConnection, Album, AlbumConnection, Genre, AlbumGenre, SongGenre, SongLike, AlbumLike
from .forms import SongForm, SongRolesForm
from django.shortcuts import redirect
def song_detail(request, slug):
   song = get_object_or_404(Song, slug=slug)

   conn = (
      SongConnection.objects
      .filter(song=song)
      .select_related("artist")
   )
   likes_obects = SongLike.objects.filter(song=song)
   likes = {
        "count": likes_obects.count(),
        "users": likes_obects.values_list("user__id", flat=True)
   }

   genres = SongGenre.objects.filter(song=song).select_related("genre")

   print(genres) 
   return render(request, "music/song_detail.html", {
      "song": song,
      "conns": conn,
      "genres": genres,
      "likes": likes,
   })






def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)

    conns = (
        AlbumConnection.objects
        .filter(album=album)
        .select_related("artist")
    )
    likes_obects = AlbumLike.objects.filter(album=album)
    likes = {
            "count": likes_obects.count(),
            "users": likes_obects.values_list("user__id", flat=True)
    }
    artist_roles = {}
    for conn in conns:
        artist_roles.setdefault(conn.artist, []).append(conn.get_role_display())

    songs = Song.objects.filter(album=album)
    print(artist_roles)
    return render(request, "music/album_detail.html", {
        "album": album,
        "artist_roles": artist_roles,
        "songs": songs,
        "likes": likes,
    })



def song_create(request):
    if request.method == "POST":
        song_form = SongForm(request.POST, request.FILES)
        roles_form = SongRolesForm(request.POST)

        if song_form.is_valid() and roles_form.is_valid():
            song = song_form.save()

            # для каждой роли создаём SongConnection
            for role_code, artists in roles_form.cleaned_data.items():
                for artist in artists:
                    SongConnection.objects.create(
                        song=song,
                        artist=artist,
                        role=role_code
                    )

            return redirect(song.get_absolute_url())
    else:
        song_form  = SongForm()
        roles_form = SongRolesForm()

    return render(request, "music/song_create.html", {
        "song_form":  song_form,
        "roles_form": roles_form,
    })


def song_like_toggle(request, slug):
    """
    Если пользователь ещё не лайкнул песню — создаём SongLike.
    Если лайк уже есть — удаляем его (т.е. «тумбл»).
    """
    song = get_object_or_404(Song, slug=slug)
    like_qs = SongLike.objects.filter(user=request.user, song=song)

    if like_qs.exists():
        like_qs.delete()
    else:
        SongLike.objects.create(user=request.user, song=song)

    return redirect(song.get_absolute_url())

def album_like_toggle(request, slug):
    album = get_object_or_404(Album, slug=slug)
    like_qs = AlbumLike.objects.filter(user=request.user, album=album)

    if like_qs.exists():
        like_qs.delete()
    else:
        AlbumLike.objects.create(user=request.user, album=album)

    return redirect(album.get_absolute_url())

# Create your views here.
