Using the application
=====================

Start the application by following the steps in the project
``README.md`` (either in a virtual environment or with Docker), then
open http://127.0.0.1:8000/ in a browser. The home page redirects to the
notes list.

Pages
-----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - URL
     - What it does
   * - ``/notes/``
     - Lists every note, newest first.
   * - ``/notes/note/new/``
     - Shows a form for creating a note.
   * - ``/notes/note/<id>/``
     - Shows a single note.
   * - ``/notes/note/<id>/edit/``
     - Shows a form for editing a note.
   * - ``/notes/note/<id>/delete/``
     - Asks for confirmation, then deletes the note.
   * - ``/admin/``
     - The Django admin site (requires a superuser account).

Running the tests
-----------------

From the ``sticky_notes`` folder run::

    python manage.py test notes
