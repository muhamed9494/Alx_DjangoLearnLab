from django.urls import path
from . import views
from .views import BookListView, BookDetailView


urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # Retrieve a book by ID
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),  # Create a new book
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),  # Update a book
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),  # Delete a book
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
