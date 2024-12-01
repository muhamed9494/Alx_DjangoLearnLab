from django.urls import path
from .views import BookListView, BookCreateView, BookDetailView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # View, update, delete a single book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Add a new book
]
