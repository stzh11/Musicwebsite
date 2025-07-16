from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts           import get_object_or_404, redirect, render
from django.urls                import reverse
from django.contrib.contenttypes.models import ContentType
from .forms                     import EditSuggestionForm
from .models                    import EditSuggestion
from music.models               import Song

@login_required
def suggest_song_edit(request, slug):
    """
    Позволяет любому пользователю предложить правку у поля песни.
    """
    song = get_object_or_404(Song, slug=slug)

    if request.method == "POST":
        form = EditSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.object_type    = ContentType.objects.get_for_model(song)
            suggestion.object_id      = song.id
            suggestion.suggested_by   = request.user
            suggestion.status         = EditSuggestion.Status.PENDING
            suggestion.save()
            return redirect(song.get_absolute_url())
    else:
        form = EditSuggestionForm()

    return render(request, "suggestions/suggest_song_edit.html", {
        "song": song,
        "form": form,
    })


def is_moderator(user):
    # тут вы можете проверить флаг is_staff или группы
    return user.is_staff

def moderate_song_edits(request):
    """
    Список всех предложений для песен. Модератор может
    принять или отклонить каждое.
    """
    edits = EditSuggestion.objects.filter(
        object_type=ContentType.objects.get_for_model(Song),
        status=EditSuggestion.Status.PENDING
    ).order_by("created_at")

    if request.method == "POST":
        action = request.POST.get("action")       # "approve" или "reject"
        edit_id = request.POST.get("edit_id")
        edit    = get_object_or_404(EditSuggestion, pk=edit_id, status=EditSuggestion.Status.PENDING)

        if action == "approve":
            # применяем правку
            song = edit.content_object
            setattr(song, edit.field_name, edit.new_value)
            song.save()

            edit.status       = EditSuggestion.Status.APPROVED
            edit.moderated_by = request.user
            edit.save()

        elif action == "reject":
            edit.status       = EditSuggestion.Status.REJECTED
            edit.moderated_by = request.user
            edit.save()

        return redirect(reverse("moderate-song-edits"))

    return render(request, "suggestions/moderate_song_edits.html", {
        "edits": edits,
    })
