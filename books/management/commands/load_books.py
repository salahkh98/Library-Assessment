import json
import os
import pandas as pd
from django.core.management.base import BaseCommand
# from your_app.models import Book, Author  # Adjust your model import path
from authors.models import Author
from books.models import Book
CHUNK_SIZE = 1000  # Process in chunks of 1000

class Command(BaseCommand):
    help = 'Load books and authors from JSON files into the database line by line'

    def handle(self, *args, **kwargs):
        self.load_authors()
        self.load_books()

    def load_authors(self):
        authors_file_path = r'D:\datasets\authors.json'  # Absolute path to authors.json
        with open(authors_file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if idx >= 2300:  # Stop after processing 300 authors
                    break
                try:
                    author_data = json.loads(line.strip())  # Load a single author entry
                    self.process_author(author_data)
                except json.JSONDecodeError as e:
                    self.stderr.write(self.style.ERROR(f"JSON decode error in authors: {e}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing author data: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully loaded authors'))

    def process_author(self, author_data):
        try:
            # Create and save an Author instance
            author = Author.objects.create(
                author_id = author_data.get('id'),
                name=author_data.get('name', 'N/A'),
                image_url =author_data.get('image_url' , 'N/A')

            )
            self.stdout.write(self.style.SUCCESS(f"Created Author {author.name}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating author: {e}"))

    def load_books(self):
        books_file_path = r'D:\datasets\books.json'  # Absolute path to books.json
        with open(books_file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if idx >= 2300:  # Stop after processing 300 books
                    break
                try:
                    book_data = json.loads(line.strip())  # Load a single book entry
                    self.process_book(book_data)
                except json.JSONDecodeError as e:
                    self.stderr.write(self.style.ERROR(f"JSON decode error in books: {e}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing book data: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully loaded books'))

    def process_book(self, book_data):
        try:
            author_id = book_data['authors'][0]['id']
            author = Author.objects.filter(id=author_id).first()
            if not author:
                self.stderr.write(self.style.ERROR(f"Author not found for book {book_data['title']}"))
                return

            # Create and save a Book instance
            book = Book.objects.create(
                title=book_data.get('title'),
                description = book_data.get('description'),
                author=author,
                isbn=book_data.get('isbn', ''),
                cover_image=book_data.get('image_url', ''),
            )
            self.stdout.write(self.style.SUCCESS(f"Created Book {book.title}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating book: {e}"))