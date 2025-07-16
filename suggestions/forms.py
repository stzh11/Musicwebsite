from django import forms
from .models import EditSuggestion

class EditSuggestionForm(forms.ModelForm):
    class Meta:
        model = EditSuggestion
        fields = ["field_name", "new_value"]
        widgets = {
            "field_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Например: title, description, cover, lyrics"}),
            "new_value": forms.Textarea(attrs={"class": "form-textarea", "rows": 3}),
        }