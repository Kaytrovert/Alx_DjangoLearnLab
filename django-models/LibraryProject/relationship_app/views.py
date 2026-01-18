from django.shortcuts import render
from django.views.generic import DetailView
from relationship_app.models import Book, Library

# Create your views here.

# Function-based view: List all books
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Displays book titles and their authors.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view: Display library details
class LibraryDetailView(DetailView):
    """
    Class-based view using DetailView to display details for a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
