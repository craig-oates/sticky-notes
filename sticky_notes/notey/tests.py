from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note, Category
from datetime import datetime
from django.urls import reverse


# Unit Tests for Models (in models.py)
# ==============================================================================

class NoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="thefancytestpasswordtest",
        )
        self.category = Category.objects.create(
            name="orange", hex_value="fbae3c"
        )
        self.note = Note.objects.create(
            user=self.user,
            title="unit_test",
            content="This is some test content.",
            created_at=datetime.now(),
            category=self.category,
        )

    def test_note_has_user(self):
        test_note = Note.objects.first()
        self.assertEqual(test_note.user.username, "testuser")

    def test_note_has_title(self):
        test_note = Note.objects.first()
        self.assertEqual(test_note.title, "unit_test")

    def test_note_has_content(self):
        test_note = Note.objects.get(id=1)
        self.assertEqual(test_note.content, "This is some test content.")

    def test_note_has_category_name(self):
        test_note = Note.objects.get(id=1)
        self.assertEqual(test_note.category.name, "orange")

    def test_note_has_category_hex_value(self):
        test_note = Note.objects.get(id=1)
        self.assertEqual(test_note.category.hex_value, "fbae3c")

    def test_note_has_created_at(self):
        test_note = Note.objects.get(id=1)
        self.assertIsNotNone(test_note.created_at)

    # TODO -- TEST CATEGORY CLASS

# Unit Tests for Views (in views.py)
# ==============================================================================


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="thefancytestpasswordtest",
        )
        self.category = Category.objects.create(
            name="orange", hex_value="fbae3c"
        )
        self.note = Note.objects.create(
            user=self.user,
            title="unit_test",
            content="This is some test content.",
            created_at=datetime.now(),
            category=self.category,
        )

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    # TODO -- TEST VIEWS IN VIEWS.PY FILE.
