from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer

# Book List View with filtering, searching, and ordering capabilities
class BookListView(ListAPIView):
    """
    API View to list all books with filtering, searching, and ordering.

    Query Parameters:
    - title: Filter by book title.
    - author__name: Filter by author's name.
    - publication_year: Filter by year of publication.
    - search: Search by title or author's name.
    - ordering: Order by title or publication year (default is title, use - for descending order).

    Example Requests:
    - /api/books/?title=python    # Filters books with 'python' in the title.
    - /api/books/?search=python   # Search books with 'python' in the title or author's name.
    - /api/books/?ordering=-title # Order books by title in descending order.
    """
    queryset = Book.objects.all()  # All book objects
    serializer_class = BookSerializer  # Serializer used to convert query results to JSON format

    # Set up the backends for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Fields that can be used for filtering
    filterset_fields = ['title', 'author__name', 'publication_year']
    
    # Fields that can be searched
    search_fields = ['title', 'author__name']
    
    # Fields that can be used for ordering
    ordering_fields = ['title', 'publication_year']
    
    # Default ordering by title
    ordering = ['title']

    # Permissions - allow read-only access, but authentication required for changes
    permission_classes = [IsAuthenticatedOrReadOnly]

# Book Create View to add new books (only accessible to authenticated users)
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can add books

# Book Detail View for retrieving, updating, or deleting a book
class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Auth required for update/delete
