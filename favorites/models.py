from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)  # Link to the book
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the favorite was added

    class Meta:
        unique_together = ('user', 'book')  # Ensure a user can favorite a book only once

    def __str__(self):
        return f"{self.user.username} favorites {self.book.title}"  # Return a meaningful string