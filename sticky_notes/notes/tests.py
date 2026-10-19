# notes/tests.py
from django.test import TestCase
from django.urls import reverse

from .models import Note
from .forms import NoteForm


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        """Create a Note object for testing."""
        Note.objects.create(
            title="Test Note",
            content="This is a test note.",
        )

    def test_note_has_title(self):
        """A Note object should have the expected title."""
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, "Test Note")

    def test_note_has_content(self):
        """A Note object should have the expected content."""
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, "This is a test note.")

    def test_note_str_returns_title(self):
        """__str__ should return the note title."""
        note = Note.objects.get(id=1)
        self.assertEqual(str(note), "Test Note")

    def test_note_ordering_is_newest_first(self):
        """Notes should be ordered by created_at descending."""
        Note.objects.create(title="Older Note", content="...")
        Note.objects.create(title="Newest Note", content="...")
        first_note = Note.objects.first()
        self.assertEqual(first_note.title, "Newest Note")

    def test_get_absolute_url(self):
        """get_absolute_url should return the detail URL."""
        note = Note.objects.get(id=1)
        expected_url = reverse("notes:note_detail", kwargs={"pk": note.pk})
        self.assertEqual(note.get_absolute_url(), expected_url)


class NoteViewTest(TestCase):
    """Tests for the Note views."""

    def setUp(self):
        """Create a Note object for view tests."""
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
        )

    def test_note_list_view(self):
        """The note list view should return 200 and contain the note."""
        response = self.client.get(reverse("notes:note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertTemplateUsed(response, "notes/note_list.html")

    def test_note_detail_view(self):
        """The detail view should return 200 and show the note content."""
        response = self.client.get(
            reverse("notes:note_detail", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "This is a test note.")
        self.assertTemplateUsed(response, "notes/note_detail.html")

    def test_note_detail_view_404_for_missing_note(self):
        """Requesting a non-existent note should return 404."""
        response = self.client.get(
            reverse("notes:note_detail", kwargs={"pk": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_note_create_view_get(self):
        """GET on the create view should render the form."""
        response = self.client.get(reverse("notes:note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_form.html")

    def test_note_create_view_post(self):
        """POST on the create view should create a new note."""
        response = self.client.post(
            reverse("notes:note_create"),
            {"title": "New Note", "content": "New content"},
        )
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(title="New Note")
        self.assertEqual(new_note.content, "New content")

    def test_note_update_view_get(self):
        """GET on the update view should render the form with data."""
        response = self.client.get(
            reverse("notes:note_update", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_update_view_post(self):
        """POST on the update view should modify the note."""
        response = self.client.post(
            reverse("notes:note_update", kwargs={"pk": self.note.pk}),
            {"title": "Updated Title", "content": "Updated content"},
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")
        self.assertEqual(self.note.content, "Updated content")

    def test_note_delete_view_get(self):
        """GET on the delete view should show a confirmation page."""
        response = self.client.get(
            reverse("notes:note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_note_delete_view_post(self):
        """POST on the delete view should remove the note."""
        response = self.client.post(
            reverse("notes:note_delete", kwargs={"pk": self.note.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 0)


class NoteFormTest(TestCase):
    """Tests for the NoteForm."""

    def test_form_valid_with_title_and_content(self):
        """A form with both fields should be valid."""
        form = NoteForm(data={"title": "Title", "content": "Content"})
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        """A form missing a title should be invalid."""
        form = NoteForm(data={"title": "", "content": "Content"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_invalid_without_content(self):
        """A form missing content should be invalid."""
        form = NoteForm(data={"title": "Title", "content": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_form_saves_note(self):
        """A valid form should create a Note instance."""
        form = NoteForm(data={"title": "Title", "content": "Content"})
        self.assertTrue(form.is_valid())
        note = form.save()
        self.assertEqual(note.title, "Title")
        self.assertEqual(Note.objects.count(), 1)


class NoteURLTest(TestCase):
    """Tests for URL patterns."""

    def test_home_url_redirects_to_note_list(self):
        """The project home page should lead to the notes list."""
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("notes:note_list"))

    def test_note_list_url_resolves(self):
        """The list URL should resolve to the correct view."""
        self.assertEqual(reverse("notes:note_list"), "/notes/")

    def test_note_create_url_resolves(self):
        """The create URL should resolve to the correct view."""
        self.assertEqual(reverse("notes:note_create"), "/notes/note/new/")

    def test_note_detail_url_resolves(self):
        """The detail URL should resolve with a pk."""
        url = reverse("notes:note_detail", kwargs={"pk": 1})
        self.assertEqual(url, "/notes/note/1/")

    def test_note_update_url_resolves(self):
        """The update URL should resolve with a pk."""
        url = reverse("notes:note_update", kwargs={"pk": 1})
        self.assertEqual(url, "/notes/note/1/edit/")

    def test_note_delete_url_resolves(self):
        """The delete URL should resolve with a pk."""
        url = reverse("notes:note_delete", kwargs={"pk": 1})
        self.assertEqual(url, "/notes/note/1/delete/")
