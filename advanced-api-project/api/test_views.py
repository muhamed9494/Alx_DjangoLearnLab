from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Author, Book
from django.contrib.auth.models import User

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()

        # Authenticate the test client
        self.client.login(username="testuser", password="testpassword")

        # Create test data
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Sample Book",
            publication_year=2022,
            author=self.author
        )
        self.book_data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        self.base_url = '/api/books/'

    def test_create_book(self):
        print("Testing POST to create a book...")
        response = self.client.post(self.base_url, self.book_data, format='json')
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])

    def test_list_books(self):
        print("Testing GET for book list...")
        response = self.client.get(self.base_url)
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        print(f"Testing GET for a single book with ID {self.book.id}...")
        response = self.client.get(f'{self.base_url}{self.book.id}/')
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        print(f"Testing PUT to update the book with ID {self.book.id}...")
        updated_data = {"title": "Updated Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.put(f'{self.base_url}{self.book.id}/', updated_data, format='json')
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_delete_book(self):
        print(f"Testing DELETE to remove the book with ID {self.book.id}...")
        response = self.client.delete(f'{self.base_url}{self.book.id}/')
        print(f"Response status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        print("Testing GET with filtering by title...")
        response = self.client.get(self.base_url, {'title': 'Sample Book'})
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        print("Testing GET with search functionality...")
        response = self.client.get(f'{self.base_url}?search=Sample')
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        print("Testing GET with ordering by publication year...")
        response = self.client.get(f'{self.base_url}?ordering=publication_year')
        print(f"Response status: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
