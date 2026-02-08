from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from .models import Book, Library, Author
from .forms import BookForm

# Permission names (from relationship_app.Book Meta): can_view, can_create, can_edit, can_delete.
# Groups: Viewers (can_view), Editors (can_view, can_create, can_edit), Admins (all four).

# Function-based view: List all books (requires can_view permission)
@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Displays book titles and their authors. Requires can_view permission.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view: Display library details (requires can_view permission)
class LibraryDetailView(PermissionRequiredMixin, DetailView):
    """
    Class-based view using DetailView to display details for a specific library.
    Requires can_view permission.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    permission_required = 'relationship_app.can_view'
    raise_exception = True


# User registration view
def register(request):
    """
    Function-based view for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role checking functions
def is_admin(user):
    """Check if user has Admin role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    """Admin view accessible only to users with Admin role."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian view accessible only to users with Librarian role."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """Member view accessible only to users with Member role."""
    return render(request, 'relationship_app/member_view.html')


# Book CRUD views: use Django forms and ORM only (no raw SQL) to prevent SQL injection
# and validate/sanitize user input. Templates include {% csrf_token %} for CSRF protection.
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """Add a new book. Uses BookForm for validation/sanitization; ORM only."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """Edit an existing book. Uses BookForm; get_object_or_404 uses parameterized lookup."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """Delete a book. Uses get_object_or_404 (parameterized); POST confirmed with CSRF."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
