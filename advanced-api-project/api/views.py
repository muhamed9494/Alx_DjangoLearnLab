# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Import permission classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer


# View to list all books (read-only access for unauthenticated users)
class BookListView(APIView):
    # Apply the IsAuthenticatedOrReadOnly permission to allow read-only for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


# View to retrieve a single book by ID
class BookDetailView(APIView):
    # Apply the IsAuthenticatedOrReadOnly permission to allow read-only for unauthenticated users
    permission_classes = [IsAuthenticatedOrReadOnly]

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
