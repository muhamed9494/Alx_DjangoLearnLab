from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns in the admin list view
    search_fields = ('title', 'author')  # Enable search functionality
    list_filter = ('publication_year',)  # Filter options for publication year
