# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from books.models import Book  # Ensure you import Book
# import numpy as np

# def get_recommendations(favorite_books, num_recommendations=5):
#     if not favorite_books:
#         return []  # Early exit if there are no favorite books

#     # Get all books in your library to compare against favorites
#     favorite_ids = [book.id for book in favorite_books]
#     all_books = Book.objects.exclude(id__in=favorite_ids)  # Exclude favorite books
#     all_books_list = list(all_books)  # Convert QuerySet to list

#     # Check if there are any books to recommend from
#     if not all_books_list:
#         return []  # No other books to recommend

#     # Get descriptions for the favorite books and handle empty descriptions
#     favorite_descriptions = [book.description for book in favorite_books if book.description]
#     book_descriptions = [book.description for book in all_books_list if book.description]

#     # Combine descriptions for TF-IDF processing
#     combined_descriptions = favorite_descriptions + book_descriptions

#     # Enhance TF-IDF Vectorizer with parameters
#     vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
#     tfidf_matrix = vectorizer.fit_transform(combined_descriptions)

#     # Calculate cosine similarity matrix
#     cosine_sim = cosine_similarity(tfidf_matrix)

#     # Collect recommendations based on similarity to favorites
#     recommendations = []

#     for idx in range(len(favorite_descriptions)):
#         # Get similarities for each favorite book with the rest of the library
#         similar_indices = cosine_sim[idx].argsort()[-(num_recommendations + 1):-1]  # Exclude the favorite itself
        
#         for sim_index in similar_indices:
#             similarity_score = cosine_sim[idx, sim_index]
#             if similarity_score > 0.1:  # Apply a threshold for similarity
#                 recommendations.append((all_books_list[sim_index], similarity_score))

#     # Filter recommendations to ensure they are not in favorites and avoid duplicates
#     unique_recommendations = {}
#     for book, score in recommendations:
#         if book.id not in favorite_ids:
#             if book.id not in unique_recommendations:
#                 unique_recommendations[book.id] = (book.title, score)

#     # Sort recommendations by similarity score
#     sorted_recommendations = sorted(unique_recommendations.values(), key=lambda x: x[1], reverse=True)

#     # Return top N recommendations, or all if less than N
#     return [title for title, _ in sorted_recommendations[:num_recommendations]
#             if title]  # Ensure we only return valid titles


from django.core.exceptions import ValidationError
from django.utils import timezone
from gensim.models import Word2Vec  # Assuming Word2Vec user embedding model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book  # Ensure you import Book
import numpy as np

# Load your pre-trained Word2Vec model here
# word2vec_model = Word2Vec.load('path_to_your_model') # Uncomment and load your model

def get_word2vec_embeddings(descriptions):
    """
    Convert descriptions to Word2Vec embeddings.
    """
    embeddings = []
    for desc in descriptions:
        if desc:  # Check if description is not empty
            words = desc.split()  # Simple tokenization, consider using a better tokenizer
            # Generate the embedding by averaging word vectors
            vec = np.mean([word2vec_model.wv[word] for word in words if word in word2vec_model.wv], axis=0)
            embeddings.append(vec if vec.size else np.zeros(word2vec_model.vector_size))  # Handle empty vectors
        else:
            embeddings.append(np.zeros(word2vec_model.vector_size))  # Handle empty description
    return np.array(embeddings)

def get_recommendations(favorite_books, num_recommendations=5, tfidf_max_features=5000, similarity_threshold=0.1):
    if not favorite_books:
        return []  # Early exit if there are no favorite books

    # Get all books in your library to compare against favorites
    favorite_ids = [book.id for book in favorite_books]
    all_books = Book.objects.exclude(id__in=favorite_ids)  # Exclude favorite books
    all_books_list = list(all_books)  # Convert QuerySet to list

    # Check if there are any books to recommend from
    if not all_books_list:
        return []  # No other books to recommend

    # Get descriptions for the favorite books and handle empty descriptions
    favorite_descriptions = [book.description for book in favorite_books if book.description]
    book_descriptions = [book.description for book in all_books_list if book.description]

    # Handle case when there are no descriptions
    if not favorite_descriptions or not book_descriptions:
        return []  # No descriptions to process

    # Combine descriptions for TF-IDF processing
    combined_descriptions = favorite_descriptions + book_descriptions

    # Enhance TF-IDF Vectorizer with parameters
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=tfidf_max_features)
    tfidf_matrix = vectorizer.fit_transform(combined_descriptions)

    # Calculate cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Collect recommendations based on similarity to favorites
    recommendations = []

    for idx in range(len(favorite_descriptions)):
        # Get similarities for each favorite book with the rest of the library
        similar_indices = cosine_sim[idx].argsort()[-(num_recommendations + 1):-1]  # Exclude the favorite itself
        
        for sim_index in similar_indices:
            similarity_score = cosine_sim[idx, sim_index]
            if similarity_score > similarity_threshold:  # Apply a threshold for similarity
                recommendations.append((all_books_list[sim_index], similarity_score))

    # Filter recommendations to ensure they are not in favorites and avoid duplicates
    unique_recommendations = {}
    for book, score in recommendations:
        if book.id not in favorite_ids:
            if book.id not in unique_recommendations:
                unique_recommendations[book.id] = (book.title, score)

    # Sort recommendations by similarity score
    sorted_recommendations = sorted(unique_recommendations.values(), key=lambda x: x[1], reverse=True)

    # Return top N recommendations, or all if less than N
    return [title for title, _ in sorted_recommendations[:num_recommendations] if title]  # Ensure we only return valid titles

# Example usage
# recommended_titles = get_recommendations(favorite_books, num_recommendations=5)
