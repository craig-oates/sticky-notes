from django.urls import path
from .views import (
    # Home/Index Section
    index,
    # User/Account Section
    register,
    user_login,
    user_logout,
    user_delete,
    # 'Sticky-Note' Section
    note_list,
    note_detail,
    note_create,
    note_update,
    note_delete,
    # Category Section
    category_list,
    category_create,
    category_delete,
)

urlpatterns = [
    # Home/Index Section
    path("", index, name="index"),
    # User/Account Section
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("user/delete/", user_delete, name="user_delete"),
    # 'Sticky-Note' Section
    path("notes", note_list, name="note_list"),
    path("note/<int:pk>/", note_detail, name="note_detail"),
    path("note/new/", note_create, name="note_create"),
    path("note/<int:pk>/edit/", note_update, name="note_update"),
    path("note/<int:pk>/delete/", note_delete, name="note_delete"),
    # Category Section
    path("categories", category_list, name="category_list"),
    path("category/new/", category_create, name="category_create"),
    path("category/<int:pk>/delete/", category_delete, name="category_delete"),
]
