from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Queryset to get all books from the database
    serializer_class = BookSerializer  # Specify the serializer to use