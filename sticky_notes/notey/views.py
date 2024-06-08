from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core import management
from .models import Note, Category
from .forms import UserRegisterForm, NoteForm, CategoryForm


def index(request):
    """
    View to display the home page of the website.

    :return: Rendered template of the home/index page.
    """
    return render(request, "notey/index.html")


def register(request):
    """
    View to register with the site, make a user account.

    :param request: HTTP request object.
    :return: Rendered template of the register/signup page.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "notey/register.html", {"form": form})


def user_login(request):
    """
    View to log into the website, using the user's account details.

    :param request: HTTP request object.
    :return: Rendered template of the login page.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("note_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "notey/login.html", {"form": form})


def user_logout(request):
    """
    View to confirm the user has logged out of the website.

    :param request: HTTP request object.
    :return: Rendered template of the login page.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, "notey/logout.html")


def user_delete(request):
    """
    View for a user to delete their account.

    :param request: HTTP request object.
    :return: Rendered template of account deleted page.
    """
    if request.user.is_authenticated:
        request.user.delete()
        # This clears the session cache for the user, help reduce weirdness in
        # the browser with out-of-date session data.
        management.call_command("clearsessions")
        return render(request, "notey/user_delete.html")
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def note_list(request):
    """
    View to display a list of 'sticky-notes'.

    :param request: HTTP reqeust object.
    :return: Rendered template, contains a list of 'sticky-notes'.
    """
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user.id)
        context = {
            "notes": notes,
            "page_title": "Your Notes",
            "user": f"{request.user.first_name} {request.user.last_name}",
        }
        return render(request, "notey/note_list.html", context)
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def note_detail(request, pk):
    """
    View to display the details of the 'sticky-note'.

    :param request: HTTP request object.
    :param pk: Primary key of the Note (sticky-note).
    :return: Rendered template, containing the details of the 'sticky-note'.
    """
    if request.user.is_authenticated:
        context = {
            "note": get_object_or_404(Note, pk=pk),
            "page_title": "Note Detail",
        }
        return render(request, "notey/note_detail.html", context)
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def note_create(request):
    """
    View to create a 'sticky-note'.

    :param request: HTTP request object.
    :return: Rendered template for creating a 'sticky-note'.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = request.user
                note.save()
                messages.success(request, "Sticky Note created.")
                return redirect("note_list")
        else:
            context = {"form": NoteForm(), "page_title": "Create Note"}
            return render(request, "notey/note_form.html", context)
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def note_update(request, pk):
    """View to update an existing 'sticky-note'.

    :param request: HTTP request object.
    :param pk: Primary key of the 'sticky-note' (i.e. Note object) to be
    updated.
    :return: Rendered template for updated the specified 'sticky-note'.
    """
    if request.user.is_authenticated:
        note = get_object_or_404(Note, pk=pk)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect("note_list")
        else:
            context = {
                "form": NoteForm(instance=note),
                "page_title": "Create Note",
                "note_id": note.id,
            }
        return render(request, "notey/note_form.html", context)
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def note_delete(request, pk):
    """
    View to delete an existing 'sticky-note'.

    :param request: HTTP request object.
    :param pk: Primary key of the 'sticky-note' to be deleted.
    :return: Redirect to the notes list after deletion.
    """
    if request.user.is_authenticated:
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return redirect("/notes")
    else:
        messages.error(request, "You are not logged in.")
        return redirect("login")


def category_list(request):
    """
    View to display a list of categories ('sticky-note' colours).

    :param request: HTTP reqeust object.
    :return: Rendered template, contains a list of categories.
    """
    if request.user.is_superuser:
        categories = Category.objects.all()
        context = {
            "categories": categories,
            "page_title": "Categories",
            "form": CategoryForm(),
        }
        return render(request, "notey/categories.html", context)
    else:
        if request.user.is_authenticated:
            messages.error(request, "You are not authorised to view that.")
            return redirect("/notes")
        else:
            messages.error(request, "You are not logged in.")
        return redirect("login")


def category_create(request):
    """
    View to create a 'sticky-note' category.

    :param request: HTTP request object.
    :return: Redirect to the category list after category creation.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.save()
                messages.success(request, "Category created.")
                return redirect("/categories")
        else:
            if request.user.is_authenticated:
                messages.error(request, "You are not authorised to view that.")
                return redirect("/notes")
            else:
                messages.error(request, "You are not logged in.")
            return redirect("login")


def category_delete(request, pk):
    """
    View to delete an existing 'sticky-note' category.

    :param request: HTTP request object.
    :param pk: Primary key of the category to be deleted.
    :return: Redirect to the category list after deletion.
    """
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect("/categories")
    else:
        if request.user.is_authenticated:
            messages.error(request, "You are not authorised to view that.")
            return redirect("/notes")
        else:
            messages.error(request, "You are not logged in.")
        return redirect("login")
