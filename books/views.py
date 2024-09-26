from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from .permissions import IsBookOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# GET /books - List all books, no authentication required
class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned books to a given search query,
        by filtering against a 'search' query parameter in the URL.
        """
        queryset = Book.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |  # Search in title
                Q(author__first_name__icontains=search_query) |  # Search in author's first name
                Q(author__last_name__icontains=search_query)  # Search in author's last name
            )
        return queryset

    def perform_create(self, serializer):
        # Automatically set the user who added the book
        serializer.save(user=self.request.user)



# GET /books/:id - Retrieve a specific book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsBookOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to handle specific book retrieval.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update an existing book (protected).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a book (protected).
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


