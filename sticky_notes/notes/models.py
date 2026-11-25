"""Database models for the notes app.

The app stores a single kind of object, :class:`Note`, which represents
one sticky note on the board.
"""
from django.db import models
from django.urls import reverse


class Note(models.Model):
    """A single sticky note.

    Notes are ordered newest first by default.

    :ivar title: Short title of the note (maximum 255 characters).
    :ivar content: Body text of the note.
    :ivar created_at: Date and time the note was created. Set
        automatically when the note is first saved.
    :ivar updated_at: Date and time the note was last modified. Updated
        automatically on every save.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model options: show the most recently created notes first."""

        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return the note title as its string representation.

        :returns: The title of the note.
        :rtype: str
        """
        return self.title

    def get_absolute_url(self) -> str:
        """Return the canonical URL for this note.

        :returns: The path of the note's detail page, for example
            ``/notes/note/1/``.
        :rtype: str
        """
        return reverse("notes:note_detail", kwargs={"pk": self.pk})
