from collections import defaultdict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Song, SongConnection, Album, AlbumConnection, Genre, AlbumGenre, SongGenre, SongLike, AlbumLike, Annotation
from .forms import SongForm, SongRolesForm, AnnotationForm
from django.shortcuts import redirect
from comments.forms import CommentForm
import html
from django.utils.safestring import mark_safe

def song_detail(request, slug):
   song = get_object_or_404(Song, slug=slug)
   form = CommentForm()
   conn = (
      SongConnection.objects
      .filter(song=song)
      .select_related("artist")
   )
   annotations = (
       Annotation.objects
       .filter(song=song)
       .order_by("start_idx")
   )
   highlighted = highlight_lyrics_with_annotations(song.lyrics, annotations) 
   likes_obects = SongLike.objects.filter(song=song)
   likes = {
        "count": likes_obects.count(),
        "users": likes_obects.values_list("user__id", flat=True)
   }
   print(song.lyrics[593:688])
   genres = SongGenre.objects.filter(song=song).select_related("genre")
   return render(request, "music/song_detail.html", {
      "song": song,
      "conns": conn,
      "annotations": annotations,
      "highlighted_lyrics": highlighted,
      "genres": genres,
      "likes": likes,
      "form": form,
      "annotation_form": AnnotationForm(),
   })



def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)
    form = CommentForm()
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
        "form": form,
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



def highlight_lyrics_with_annotations(lyrics: str, annotations):
    # Сортируем аннотации по start_idx
    anns = sorted(annotations, key=lambda a: a.start_idx)
    parts = []
    last_pos = 0

    for ann in anns:
        # Экранируем текст до аннотации
        parts.append(html.escape(lyrics[last_pos:ann.start_idx]))
        # Экранируем фрагмент и оборачиваем в span
        fragment = html.escape(lyrics[ann.start_idx:ann.end_idx])
        parts.append(
            f'<span class="annotation" '
            f'data-ann-id="{ann.annotation_id}" '
            f'title="{html.escape(ann.description)}">'
            f'{fragment}</span>'
        )
        last_pos = ann.end_idx

    # Добавляем остаток текста
    parts.append(html.escape(lyrics[last_pos:]))
    return mark_safe("".join(parts))

def add_song_annotation(request, slug):
    song = get_object_or_404(Song, slug=slug)
    print("add_song_ann by slug ---", song.slug)
    if request.method == "POST":
        print("POST request received for annotation")
        form = AnnotationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            ann = form.save(commit=False)
            ann.song = song
            ann.creator = request.user
            ann.save()
            print("Annotation saved:", ann)

            return redirect(song.get_absolute_url())
    else:
        form = AnnotationForm()

    return render(request, "music/annotation_form.html", {'form': form, 'song': song})
