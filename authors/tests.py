from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author

class AuthorAPITests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a second user for testing author ownership
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')

        # Create an author instance for testing
        self.author = Author.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            biography='A sample biography.',
            date_of_birth='1980-01-01'
        )

    def test_get_authors(self):
        """Test retrieving the list of authors."""
        response = self.client.get(reverse('author-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one author

    def test_create_author(self):
        """Test creating a new author."""
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'biography': 'Another sample biography.',
            'date_of_birth': '1990-02-02',
        }
        response = self.client.post(reverse('author-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)  # Should now have 2 authors

    def test_get_author_detail(self):
        """Test retrieving a specific author by ID."""
        response = self.client.get(reverse('author-detail', args=[self.author.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.author.first_name)

    def test_update_author(self):
        """Test updating an existing author."""
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        data = {
            'first_name': 'Johnathan',
            'last_name': 'Doe',
            'biography': 'Updated biography.',
            'date_of_birth': '1980-01-01',
        }
        response = self.client.put(reverse('author-detail', args=[self.author.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()  # Refresh the author instance from the database
        self.assertEqual(self.author.first_name, 'Johnathan')

    def test_delete_author(self):
        """Test deleting an author."""
        self.client.login(username='testuser', password='testpassword')  # Log in the user
        response = self.client.delete(reverse('author-detail', args=[self.author.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)  # Author should be deleted

    def test_update_author_other_user(self):
        """Test that a user cannot update another user's author."""
        self.client.login(username='otheruser', password='testpassword')  # Log in the other user
        data = {
            'first_name': 'Malcolm',
            'last_name': 'Doe',
            'biography': 'Malcolm biography.',
            'date_of_birth': '1980-01-01',
        }
        response = self.client.put(reverse('author-detail', args=[self.author.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden

    def test_delete_author_other_user(self):
        """Test that a user cannot delete another user's author."""
        self.client.login(username='otheruser', password='testpassword')  # Log in the other user
        response = self.client.delete(reverse('author-detail', args=[self.author.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden

