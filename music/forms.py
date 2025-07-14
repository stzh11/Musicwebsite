# music/views.py
from django import forms
from django.forms import inlineformset_factory
from .models import Song, SongConnection, Annotation
from artists.models import Artist
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = [
            "title", "description", "album", "released_date",
            "lyrics", "translation_lyrics",
            "cover", "clip_url", "yandex_music_url",
        ]
        widgets = {
            "released_date": forms.DateInput(attrs={"type": "date"}),
        }

class SongRolesForm(forms.Form):
    """
    Форма для назначения артистов на роли в песне.
    Для каждой роли из SongConnection.Role создаётся поле wybor артистов.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Общий queryset всех артистов
        artists_qs = Artist.objects.all()

        # Для каждой роли из TextChoices динамически создаём поле
        for role_code, role_label in SongConnection.Role.choices:
            self.fields[role_code] = forms.ModelMultipleChoiceField(
                queryset=artists_qs,
                required=False,
                label=role_label,
                widget=forms.SelectMultiple(attrs={
                    "class": "block w-full border rounded p-2",
                    "size": 5,  # можно регулировать высоту списка
                })
            )

class AnnotationForm(forms.ModelForm):
    
    class Meta:
        model = Annotation
        fields = ["description", "photo_url", "start_idx", "end_idx"]

        widgets = {
            "start_idx": forms.HiddenInput(),
            "end_idx": forms.HiddenInput(),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Введите описание аннотации",
            }),
            "photo_url": forms.URLInput(attrs={
                "placeholder": "Ссылка на фото (необязательно)",
            })
        }