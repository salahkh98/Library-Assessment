from django.contrib import admin
from .models import Favorite
# Register your models here.
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    search_fields = ['book__title']  # Allow searching by book title

    # Optionally, you can specify other fields to display in the admin list view
    list_display = ['user', 'book', 'created_at']  # Show user, book, and created_at fields

    # If you want to filter by user, you can add list_filter
    list_filter = ['user']  # Filter by user
