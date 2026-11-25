"""Forms for the notes app."""
from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and updating :class:`~notes.models.Note` objects.

    The form exposes the ``title`` and ``content`` fields. Both are
    required, and the title is limited to 255 characters by the model.
    """

    class Meta:
        """Bind the form to the Note model and style its widgets."""

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
