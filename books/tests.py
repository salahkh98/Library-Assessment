from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from books.models import Book
from authors.models import Author

User = get_user_model()


class BookAPITests(APITestCase):
    def setUp(self):
        """
        Set up a test user, an author, and an initial book object for testing.
        """
        self.client = APIClient()

        # Create a user for authentication tests
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create another user (non-owner)
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        # Create an author for the book
        self.author = Author.objects.create(first_name='Author 1')

        # Create a book for testing
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            published_date='2023-01-01',
            isbn='1234567890123',
            user=self.user
        )

        # Endpoints to be tested
        self.book_list_url = reverse('book-list-create')
        self.book_detail_url = reverse('book-detail', args=[self.book.pk])

    # --- TEST UNPROTECTED ENDPOINTS ---

    def test_get_books_list(self):
        """
        Test that anyone (authenticated or not) can retrieve the list of books (unprotected).
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_book(self):
        """
        Test that anyone (authenticated or not) can retrieve a single book by ID (unprotected).
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- TEST PROTECTED ENDPOINTS ---

    def test_create_book_requires_authentication(self):
        """
        Test that creating a new book requires authentication.
        """
        new_book_data = {
            'title': 'New Test Book',
            'author': self.author.pk,
            'published_date': '2023-01-01',
            'isbn': '9876543210123'
        }
        # Attempt to create a book without authentication
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate and try again
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.book_list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_requires_owner(self):
        """
        Test that updating a book requires authentication and the user must be the owner.
        """
        updated_data = {
            'title': 'Updated Test Book',
            'author': self.author.pk,
            'published_date': '2023-01-01',
            'isbn': '1234567890123'
        }

        # Attempt to update without authentication
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate as the book owner
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Authenticate as another user (non-owner)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.put(self.book_detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Not the owner

    def test_delete_book_requires_owner(self):
        """
        Test that deleting a book requires authentication and the user must be the owner.
        """
        # Attempt to delete without authentication
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate as the book owner
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try deleting as another user (non-owner)
        new_book = Book.objects.create(
            title='Another Book',
            author=self.author,
            published_date='2023-01-01',
            isbn='0987654321098',
            user=self.user
        )
        book_detail_url = reverse('book-detail', args=[new_book.pk])
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_protected_endpoints(self):
        """
        Test that protected endpoints (POST, PUT, DELETE) require authentication.
        """
        new_book_data = {
            'title': 'Another New Book',
            'author': self.author.pk,
            'published_date': '2023-01-01',
            'isbn': '1111111111111'
        }

        # Test POST (Create) requires authentication
        response = self.client.post(self.book_list_url, new_book_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Test PUT (Update) works when authenticated
        updated_data = {
            'title': 'Updated Book Title',
            'author': self.author.pk,
            'published_date': '2023-01-01',
            'isbn': '1234567890123'
        }
        response = self.client.put(self.book_detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test DELETE works when authenticated as the owner
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
