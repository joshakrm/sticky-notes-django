# notes/models.py
from django.db import models
from django.urls import reverse


class Note(models.Model):
    """Model representing a single sticky note.

    Fields:
        title: Short title of the note.
        content: Body text of the note.
        created_at: Timestamp when the note was created.
        updated_at: Timestamp when the note was last modified.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return the note title as its string representation."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the canonical URL for a note instance."""
        return reverse("notes:note_detail", kwargs={"pk": self.pk})
