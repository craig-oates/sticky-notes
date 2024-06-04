# Documentation for 'User' import found at:
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-the-existing-user-model
from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """
    Represents a 'sticky-note', post

    Fields:
    - title: Charfield for the contents of the note, with a maximum length of
      255 chararcters.
    - content: TextField for the note's contents.
    - created_at: DateTimeField set to the time and date the note is created.

    Relationships:
    - user: ForeignKey representing the user/creator of the note.
    - category: ForeignKey representing the category of the note.

    Methods:
    - N/A

    Parameters:
    - models.Model: Django's base model class.
    """

    user = models.ForeignKey(
        # See comment at top of file for 'User' import.
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )


class Category(models.Model):
    """
     Represents the category of a 'sticky-note'.

     Fields:
     - hex_value: CharField representing the 'colour' of the 'sticky-note', with
       a maximum of 6 characters.
     - name: CharField representing the name of the category, with a maximum
       length of 255 characters.

     Relationships:
    - N/A

     Parameters:
     - models.Model: Django's base model class.
    """

    name = models.CharField(max_length=255)
    hex_value = models.CharField(max_length=6)
