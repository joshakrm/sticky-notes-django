"""Admin site configuration for the notes app."""
from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin configuration for the :class:`~notes.models.Note` model.

    Shows the title and timestamps in the change list, allows searching
    by title or content, and lists the newest notes first.
    """

    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
