from django.contrib import admin

# Added after the project generated.
from .models import Note
from .models import Category

admin.site.register(Note)
admin.site.register(Category)
