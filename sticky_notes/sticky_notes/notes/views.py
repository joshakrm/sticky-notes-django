# notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse

from .models import Note
from .forms import NoteForm


def note_list(request: HttpRequest) -> HttpResponse:
    """Display a list of all sticky notes."""
    notes = Note.objects.all()
    context = {
        "notes": notes,
        "page_title": "All Notes",
    }
    return render(request, "notes/note_list.html", context)


def note_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Display the details of a single note."""
    note = get_object_or_404(Note, pk=pk)
    context = {
        "note": note,
        "page_title": note.title,
    }
    return render(request, "notes/note_detail.html", context)


def note_create(request: HttpRequest) -> HttpResponse:
    """Create a new sticky note."""
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm()

    context = {
        "form": form,
        "page_title": "Create Note",
    }
    return render(request, "notes/note_form.html", context)


def note_update(request: HttpRequest, pk: int) -> HttpResponse:
    """Update an existing sticky note."""
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes:note_detail", pk=note.pk)
    else:
        form = NoteForm(instance=note)

    context = {
        "form": form,
        "note": note,
        "page_title": f"Edit: {note.title}",
    }
    return render(request, "notes/note_form.html", context)


def note_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a sticky note after confirmation."""
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("notes:note_list")

    context = {
        "note": note,
        "page_title": f"Delete: {note.title}",
    }
    return render(request, "notes/note_confirm_delete.html", context)
