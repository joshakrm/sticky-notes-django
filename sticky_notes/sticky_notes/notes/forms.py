# notes/forms.py
from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and updating Note objects."""

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter a title...",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "placeholder": "Write your note here...",
                    "rows": 6,
                }
            ),
        }