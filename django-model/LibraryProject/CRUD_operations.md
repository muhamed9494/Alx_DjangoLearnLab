# CRUD Operations for Book Model

## Create Operation
Command:

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

## Retrieve Operation
Command:

```python
retrieved_book = Book.objects.get(title="1984")
retrieved_book


## Update Operation
Command:

```python
book.title = "Nineteen Eighty-Four"
book.save()
book


## Delete Operation
Command:

```python
book.delete()
Book.objects.all()