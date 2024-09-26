from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from .permissions import IsAuthorOwnerOrReadOnly  # Ensure this permission is defined

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    GET /authors - Retrieve a list of all authors.
    POST /authors - Create a new author (protected).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow public access for GET, protected for POST

    def list(self, request, *args, **kwargs):
        """
        Override the list method to customize the response.
        """
        authors = self.get_queryset()
        serializer = self.get_serializer(authors, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a new author with the current user as the owner.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /authors/:id - Retrieve a specific author by ID.
    PUT /authors/:id - Update an existing author (protected).
    DELETE /authors/:id - Delete an author (protected).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthorOwnerOrReadOnly]  # Use the custom permission

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an existing author by ID.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update an existing author (protected).
        """
        partial = kwargs.pop('partial', False)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an author (protected).
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
