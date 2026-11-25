"""URL patterns for the notes app.

All routes are namespaced under ``notes`` and are mounted at ``/notes/``
by the project URL configuration:

* ``""`` -- list all notes (``notes:note_list``)
* ``note/new/`` -- create a note (``notes:note_create``)
* ``note/<pk>/`` -- show one note (``notes:note_detail``)
* ``note/<pk>/edit/`` -- edit a note (``notes:note_update``)
* ``note/<pk>/delete/`` -- delete a note (``notes:note_delete``)
"""
from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("note/<int:pk>/", views.note_detail, name="note_detail"),
    path("note/new/", views.note_create, name="note_create"),
    path("note/<int:pk>/edit/", views.note_update, name="note_update"),
    path("note/<int:pk>/delete/", views.note_delete, name="note_delete"),
]
