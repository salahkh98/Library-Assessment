from django.urls import path

from .views import BookListCreateView, BookDetailView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),  # List and create books
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve, update, and delete a book by ID
]