from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search functionality for the 'title' and 'author' fields
    search_fields = ['title', 'author']
    
    # Add filters for the 'publication_year' field
    list_filter = ['publication_year']

# Register the Book model with custom configurations
admin.site.register(Book, BookAdmin)