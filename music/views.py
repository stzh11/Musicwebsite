from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Song, SongConnection, Album, AlbumConnection

def song_detail(request, slug):
   song = get_object_or_404(Song, slug=slug)

   conn = (
      SongConnection.objects
      .filter(song=song)
      .select_related("artist")
   )

   return render(request, "music/song_detail.html", {
      "song": song,
      "conns": conn,
   })

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)
    conns = (
      AlbumConnection.objects
      .filter(album=album)
      .select_related("artist")
    )
    songs = (
      Song.objects
      .filter(album=album)
    )
    return render(request, "music/album_detail.html", {
        "album": album,
        "conns": conns,
        "songs": songs,
    })

# Create your views here.
