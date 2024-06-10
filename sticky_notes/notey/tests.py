from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note, Category
from datetime import datetime
from django.urls import reverse


# Unit Tests for Models (in models.py)
# ==============================================================================


class ModelTests(TestCase):
    """
    Test class for testing the classes/models in models.py file.

    Parameters:
    - django.test.TestCase: Parent class this class inherits from.
    - django.contrib.auth.models.User: Django class for creating User objects,
      typically attached to a set of 'sticky-notes'.
    - models.Note: Note class represting a 'sticky-note'.
    - models.Category: Category class representing a category the
      'sticky-notes' are stored as (i.e. hex-value).
    """

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


# Unit Tests for Views (in views.py)
# ==============================================================================


class ViewTests(TestCase):
    """
    Test class for testing the views in views.py file.

    Parameters:
    - django.test.TestCase: Parent class this class inherits from.
    - django.contrib.auth.models.User: Django class for creating User objects,
      typically attached to a set of 'sticky-notes'.
    - models.Note: Note class represting a 'sticky-note'.
    - models.Category: Category class representing a category the
      'sticky-notes' are stored as (i.e. hex-value).
    """

    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="thefancytestpassword",
        )
        self.super_user = User.objects.create_superuser(
            username="super_user",
            email="super@email.com",
            password="superuserpassword",
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

    def test_user_login_view(self):
        # Checks if user can log in, with valid account details.
        self.client.force_login(self.user)
        response = self.client.post(reverse("login"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dashboard")
        # Checks if user can log in, with invalid account details.
        self.client.login(username="non_user", password="incorrectpassword")
        response = self.client.post(reverse("login"), follow=True)
        self.assertContains(response, "Invalid username or password.")

    def test_user_logout_view(self):
        # Checks to see if user can logout of session.
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have successfully logged out.")

    def test_user_delete_view(self):
        # Checks to see if user's account can be deleted.
        self.client.force_login(self.user)
        response = self.client.post(reverse("user_delete"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your account has been deleted.")
        # Check for non-logged in users.
        visitor_response = self.client.get(reverse("user_delete"))
        self.assertEqual(visitor_response.status_code, 302)

    def test_index_view(self):
        # Checks the home/index view is reachable.
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        # Checks the register view to make sure a user account can be created.
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_note_list_view(self):
        # Checks the note_list/dashboard view, when user is logged in.
        self.client.login(username="testuser", password="thefancytestpassword")
        url = reverse("note_list")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        # Checks the note_list/dashboard view, when user is not logged in.
        self.client.logout()
        visitor_response = self.client.get(url)
        self.assertEqual(visitor_response.status_code, 302)

    def test_note_detail_view(self):
        # Checks to see if a detail view of a note can be viewed.
        self.client.force_login(self.user)
        url = reverse("note_detail", kwargs={"pk": 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Created at:")
        # Check for non-logged in users.
        self.client.logout()
        visitor_response = self.client.get(url)
        self.assertEqual(visitor_response.status_code, 302)

    def test_note_create_view(self):
        # Checks to see if a 'sticky-note' for can be accessed by user.
        self.client.force_login(self.user)
        url = reverse("note_create")
        self.client.logout()
        # Check for visitors not logged into the website, to redirect.
        visitor_response = self.client.get(url)
        self.assertEqual(visitor_response.status_code, 302)

    def test_note_update_view(self):
        # Check to see if user can update/edit a 'sticky-note'.
        # Check for logged in users.
        self.client.force_login(self.user)
        url = reverse("note_update", kwargs={"pk": 1})
        post_data = {"title": "New Updated Title",
                     "Content": "New content"}
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check for non-logged in users.
        self.client.logout()
        visitor_response = self.client.get(url)
        self.assertEqual(visitor_response.status_code, 302)

    def test_note_delete_view(self):
        # Checks to see if a 'sticky-note' for can be accessed by user.
        self.client.force_login(self.user)
        url = reverse("note_delete", kwargs={"pk": 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        # Check for visitors not logged into the website, to redirect.
        visitor_response = self.client.get(url)
        self.assertEqual(visitor_response.status_code, 302)

    def test_category_list_view(self):
        # Checks to see if category_list can be viewed.
        # User must be a super user to view this page.
        self.client.force_login(self.super_user)
        response = self.client.get(reverse("category_list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "For a list of Post-It style colour")
        self.client.logout()
        # Checks the category list page as a non-super user.
        self.client.force_login(self.user)
        not_auth_response = self.client.get(
            reverse("category_list"), follow=True
        )
        self.assertEqual(not_auth_response.status_code, 200)
        self.assertContains(
            not_auth_response, "You are not authorised to view that."
        )
        self.client.logout()
        # Check for non-logged in users.
        visitor_response = self.client.get(reverse("category_list"))
        self.assertEqual(visitor_response.status_code, 302)

    def test_category_create_view(self):
        # Checks to see if a category can be created.
        # User must be a super user to view this page.
        self.client.force_login(self.super_user)
        response = self.client.post(
            reverse("category_create"),
            data={"name": "White", "hex_value": "000000"},
            follow=True,
        )
        self.assertRedirects(response, reverse("category_list"))
        self.assertContains(response, "Category created.")
        self.client.logout()
        # Checks the category list page as a non-super user.
        self.client.force_login(self.user)
        not_auth_response = self.client.get(
            reverse("category_create"),
            data={"name": "White", "hex_value": "000000"},
            follow=True,
        )
        self.assertRedirects(not_auth_response, reverse("note_list"))
        self.assertContains(
            not_auth_response, "You are not authorised to view that."
        )
        self.client.logout()
        # # Check for non-logged in users.
        visitor_response = self.client.post(
            reverse("category_list"),
            data={"name": "White", "hex_value": "000000"},
            follow=True,
        )
        self.assertRedirects(visitor_response, reverse("login"))
        self.assertContains(visitor_response, "You are not logged in.")

    def test_category_delete_view(self):
        # Checks to see if a category can be deleted.
        # User must be a super user to view this page.
        self.client.force_login(self.super_user)
        self.client.post(
            reverse("category_create"),
            data={"name": "White", "hex_value": "000000"},
            follow=True,
        )
        url = reverse("category_delete", kwargs={"pk": 1})
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse("category_list"))
        self.assertContains(response, "Category deleted.")
        self.client.logout()
        # Checks the category list page as a non-super user.
        self.client.force_login(self.user)
        not_auth_response = self.client.get(url, follow=True)
        self.assertRedirects(not_auth_response, reverse("note_list"))
        self.assertContains(
            not_auth_response, "You are not authorised to view that."
        )
        self.client.logout()
        # # Check for non-logged in users.
        visitor_response = self.client.post(url, follow=True)
        self.assertRedirects(visitor_response, reverse("login"))
        self.assertContains(visitor_response, "You are not logged in.")
