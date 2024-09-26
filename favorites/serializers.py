from rest_framework import serializers
from .models import Favorite
from books.serializers import BookSerializer
from books.models import Book

class FavoriteSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # Allow selection from book list

    class Meta:
        model = Favorite
        fields = ['id', 'book']  # Only show book for selection
        read_only_fields = ['user']  # User will be set in the view