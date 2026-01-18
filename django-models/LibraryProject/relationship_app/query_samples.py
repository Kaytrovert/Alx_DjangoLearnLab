"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey: Query all books by a specific author
- ManyToMany: List all books in a library
- OneToOne: Retrieve the librarian for a library
"""

from relationship_app.models import Author, Book, Library, Librarian


# ForeignKey Relationship: Query all books by a specific author
def query_books_by_author(author_name):
    """
    Demonstrates ForeignKey relationship.
    Query all books written by a specific author.
    
    Args:
        author_name (str): The name of the author
    
    Returns:
        QuerySet: All books by the specified author
    """
    try:
        author = Author.objects.get(name=author_name)
        # Using filter with author object
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return Book.objects.none()


# Alternative ForeignKey query using filter
def query_books_by_author_alternative(author_name):
    """
    Alternative method: Query books using filter with ForeignKey lookup.
    """
    books = Book.objects.filter(author__name=author_name)
    return books


# ManyToMany Relationship: List all books in a library
def list_books_in_library(library_name):
    """
    Demonstrates ManyToMany relationship.
    List all books that belong to a specific library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        QuerySet: All books in the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        # Access books through the ManyToManyField
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return Book.objects.none()


# Alternative ManyToMany query using filter
def list_books_in_library_alternative(library_name):
    """
    Alternative method: Query books using filter with ManyToMany lookup.
    """
    books = Book.objects.filter(libraries__name=library_name)
    return books


# OneToOne Relationship: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    """
    Demonstrates OneToOne relationship.
    Retrieve the librarian assigned to a specific library.
    
    Args:
        library_name (str): The name of the library
    
    Returns:
        Librarian object or None: The librarian for the specified library
    """
    try:
        library = Library.objects.get(name=library_name)
        # Access librarian through the related_name "librarian" defined in Librarian model
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None


# Alternative OneToOne query using filter
def get_librarian_for_library_alternative(library_name):
    """
    Alternative method: Query librarian using filter with OneToOne lookup.
    """
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        return librarian
    except Librarian.DoesNotExist:
        return None


# Example usage functions (commented out to avoid execution errors if data doesn't exist)
"""
# Example 1: Query all books by a specific author
author_books = query_books_by_author("J.K. Rowling")
for book in author_books:
    print(f"- {book.title}")

# Example 2: List all books in a library
library_books = list_books_in_library("Central Library")
for book in library_books:
    print(f"- {book.title} by {book.author.name}")

# Example 3: Retrieve the librarian for a library
librarian = get_librarian_for_library("Central Library")
if librarian:
    print(f"Librarian: {librarian.name}")
else:
    print("No librarian assigned to this library")
"""
