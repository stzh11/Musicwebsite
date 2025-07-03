from collections import defaultdict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Song, SongConnection, Album, AlbumConnection, Genre, AlbumGenre, SongGenre
from .forms import SongForm, SongRolesForm
from django.shortcuts import redirect
def song_detail(request, slug):
   song = get_object_or_404(Song, slug=slug)

   conn = (
      SongConnection.objects
      .filter(song=song)
      .select_related("artist")
   )
   genres = SongGenre.objects.filter(song=song).select_related("genre")
   print(genres) 
   return render(request, "music/song_detail.html", {
      "song": song,
      "conns": conn,
      "genres": genres,
   })

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)

    conns = (
        AlbumConnection.objects
        .filter(album=album)
        .select_related("artist")
    )

    artist_roles = {}
    for conn in conns:
        artist_roles.setdefault(conn.artist, []).append(conn.get_role_display())

    songs = Song.objects.filter(album=album)
    print(artist_roles)
    return render(request, "music/album_detail.html", {
        "album": album,
        "artist_roles": artist_roles,
        "songs": songs,
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
# Create your views here.
