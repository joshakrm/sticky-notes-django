"""Views for the notes app.

Each view handles one step of the create, read, update and delete
(CRUD) workflow for :class:`~notes.models.Note` objects and renders a
template from ``notes/templates/notes``.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse

from .models import Note
from .forms import NoteForm


def note_list(request: HttpRequest) -> HttpResponse:
    """Display a list of all sticky notes.

    :param request: The incoming HTTP request.
    :type request: django.http.HttpRequest
    :returns: The rendered ``notes/note_list.html`` page.
    :rtype: django.http.HttpResponse
    """
    notes = Note.objects.all()
    context = {
        "notes": notes,
        "page_title": "All Notes",
    }
    return render(request, "notes/note_list.html", context)


def note_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Display the details of a single note.

    :param request: The incoming HTTP request.
    :type request: django.http.HttpRequest
    :param pk: Primary key of the note to display.
    :type pk: int
    :returns: The rendered ``notes/note_detail.html`` page.
    :rtype: django.http.HttpResponse
    :raises django.http.Http404: If no note with the given ``pk`` exists.
    """
    note = get_object_or_404(Note, pk=pk)
    context = {
        "note": note,
        "page_title": note.title,
    }
    return render(request, "notes/note_detail.html", context)


def note_create(request: HttpRequest) -> HttpResponse:
    """Create a new sticky note.

    A ``GET`` request shows an empty form. A ``POST`` request validates
    the submitted data and, if it is valid, saves the note and redirects
    to its detail page. Invalid data re-displays the form with errors.

    :param request: The incoming HTTP request.
    :type request: django.http.HttpRequest
    :returns: The rendered form, or a redirect to the new note.
    :rtype: django.http.HttpResponse
    """
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
    """Update an existing sticky note.

    A ``GET`` request shows the form pre-filled with the note's current
    values. A valid ``POST`` request saves the changes and redirects to
    the note's detail page.

    :param request: The incoming HTTP request.
    :type request: django.http.HttpRequest
    :param pk: Primary key of the note to edit.
    :type pk: int
    :returns: The rendered form, or a redirect to the updated note.
    :rtype: django.http.HttpResponse
    :raises django.http.Http404: If no note with the given ``pk`` exists.
    """
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
    """Delete a sticky note after confirmation.

    A ``GET`` request shows a confirmation page. Only a ``POST`` request
    deletes the note, after which the user is sent back to the note list.

    :param request: The incoming HTTP request.
    :type request: django.http.HttpRequest
    :param pk: Primary key of the note to delete.
    :type pk: int
    :returns: The confirmation page, or a redirect to the note list.
    :rtype: django.http.HttpResponse
    :raises django.http.Http404: If no note with the given ``pk`` exists.
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("notes:note_list")

    context = {
        "note": note,
        "page_title": f"Delete: {note.title}",
    }
    return render(request, "notes/note_confirm_delete.html", context)
