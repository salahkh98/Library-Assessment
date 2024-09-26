from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)  # Book title
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE, related_name='books')  # Link to the Author model
    description = models.TextField(default="Description not available")  # Set a default value
    isbn = models.CharField(max_length=13, unique=True)  # Unique ISBN number
    cover_image = models.URLField(blank=True, null=True)  # Optional cover image URL
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', null=True)  # User who added the book
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last updated timestamp

    def __str__(self):
        return self.title