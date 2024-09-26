from django.contrib import admin
from .models import Book
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')  # Display title and author in the admin list view
    search_fields = ('title',)  # Allow searching by title and author names

    # Optionally, you can also add filters
    list_filter = ('author',)  # Filter by author