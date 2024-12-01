from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model to convert book data into JSON format.

    Includes validation to ensure the publication year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

    # Custom validation for publication year
    def validate_publication_year(self, value):
        if value > 2024:  # Assuming 2024 as the current year for validation
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model and includes a nested BookSerializer
    to handle related books.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

