from django.urls import path
from .views import RecommendationViewSet

urlpatterns = [
    path('recommendations/', RecommendationViewSet.as_view({'get': 'list'}), name='recommendation-list'),
]
