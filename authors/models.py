from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Author(models.Model):
    author_id = models.CharField(max_length=20 ,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming a default user with ID 1 exists
    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Last updated timestamp

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['name']  # Order authors by last name

    def __str__(self):
        return f"{self.name}"  # Return full name of the author