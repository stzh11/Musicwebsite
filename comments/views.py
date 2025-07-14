# comments/views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType

from music.models import Song, Album
from .models import Comment
from .forms import CommentForm

def song_comment_create(request, slug):
    song = get_object_or_404(Song, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user

        comment.content_type = ContentType.objects.get_for_model(Song)
        comment.object_id    = song.pk

        comment.save()
    return redirect(song.get_absolute_url())


def album_comment_create(request, slug):

    album = get_object_or_404(Album, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user

        comment.content_type = ContentType.objects.get_for_model(Album)
        comment.object_id    = album.pk

        comment.save()
    return redirect(album.get_absolute_url())

# Create your views here.
