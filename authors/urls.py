from django.urls import path
from .views import AuthorListCreateView, AuthorDetailView

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),  # List and create authors
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),  # Retrieve, update, delete author
]
