from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Note, Category


class UserRegisterForm(UserCreationForm):
    """
    Form for creating a User Account on the website.

    Fields:
    - email: EmailField for the User's profile.

    Meta class:

    - Defines the model to use and the fiels to include in the User Register
      Form.

    :para forms.ModelForm: Django's ModelForm class.

    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class NoteForm(forms.ModelForm):
    """
    Form for creating and updating 'sticky-notes' (Note objects).

    Fields:
    - title: CharField for the Note's title.
    - content: TextField for the Note's content.

    Meta class:
    - Defines the model to use (Note) and the fields to include in the
    form.

    :param forms.ModelForm: Django's ModelForm class.
    """

    class Meta:
        model = Note
        fields = ["title", "content", "category"]


class CategoryForm(forms.ModelForm):
    """
    Form for creating a 'sticky-note' category.

    A category, in this instance, refers to the colour of the 'stick-note'.

    Fields:
    - name: CharField for the categories name.
    - hex_value: The hex-value of the categories colour.

    Meta class:
    -Defines the model to use (Category) and the fields to include in the form.

    :param form.ModelForm: Django's ModelForm class.
    """

    class Meta:
        model = Category
        fields = ["name", "hex_value"]
