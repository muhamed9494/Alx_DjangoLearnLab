# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Import permission classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as django_filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


filters.OrderingFilter = OrderingFilter
filters.SearchFilter = SearchFilter

# Filter class for Book model
class BookFilter(filters.FilterSet):
    """
    Filters for the Book model. The following fields can be used for filtering:
    - title: case-insensitive search for book titles.
    - author: case-insensitive search for author names.
    - publication_year: filter by the year of publication.
    """
    title = filters.CharFilter(lookup_expr='icontains') # Filter books by title (case-insensitive)
    author = filters.CharFilter(field_name='author__name', lookup_expr='icontains') # Filter books by author's name
    publication_year = filters.NumberFilter() # Filter books by publication year

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year'] # Fields that can be filtered  


# View class for listing books with filtering, searching, and ordering
class BookListView(ListCreateAPIView):
    
    #List view for the Book model, providing the following features:
    #- Filtering: Allows filtering by title, author, and publication year.
    #- Searching: Allows searching by title and author name.
    #- Ordering: Allows ordering the books by title or publication year.
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # SearchFilter from DRF
    filterset_class = BookFilter # Use the BookFilter class for filtering
    search_fields = ['title', 'author__name'] # Fields that can be searched
    ordering_fields = ['title', 'publication_year'] # Fields that can be used for ordering
    ordering = ['title']  # Default ordering by title (ascending)

    # Documentation for API behavior:
    # - Filtering can be done by providing query parameters such as:
    #     - `title=<book_title>`: Filter by title.
    #     - `author=<author_name>`: Filter by author's name.
    #     - `publication_year=<year>`: Filter by year of publication.
    # - Searching is possible using the `search` query parameter for the fields defined in `search_fields`.
    # - Ordering can be controlled with the `ordering` query parameter for fields listed in `ordering_fields`.

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


# View to retrieve a single book by ID
class BookDetailView(RetrieveUpdateDestroyAPIView):
    # Apply the IsAuthenticatedOrReadOnly permission to allow read-only for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def get(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(pk=kwargs['pk'])
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)


# View to create a new book (requires authentication)
class BookCreateView(APIView):
    # Apply the IsAuthenticated permission to require authentication for creating a book
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to update an existing book (requires authentication)
class BookUpdateView(APIView):
    # Apply the IsAuthenticated permission to require authentication for updating a book
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        book_id = request.data.get('id')  # Get the book ID from the request data
        if not book_id:
            return Response({"detail": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View to delete a book (requires authentication)
class BookDeleteView(APIView):
    # Apply the IsAuthenticated permission to require authentication for deleting a book
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('id')  # Get the book ID from the request data
        if not book_id:
            return Response({"detail": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"detail": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
