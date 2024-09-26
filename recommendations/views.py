# In your recommendations/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from .recommendation_logic import get_recommendations   # Your recommendation logic function
from favorites.models import Favorite
from rest_framework.response import Response  # Import Response here


class RecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        favorite_books = [favorite.book for favorite in favorites]
        
        recommendations = get_recommendations(favorite_books)  # Your function to get recommendations
        return Response(recommendations)
    

