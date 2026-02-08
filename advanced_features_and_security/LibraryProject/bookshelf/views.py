from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from .models import Book
from .forms import BookForm, BookSearchForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    List books; optional safe search via form. Uses ORM only (parameterized queries),
    no raw SQL, to prevent SQL injection. User input validated/sanitized by BookSearchForm.
    """
    books = Book.objects.all()
    form = BookSearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            # ORM filter is parameterized; never use string formatting for SQL.
            books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})


@permission_required('bookshelf.can_create', raise_exception=True)
def form_example(request):
    """
    Example form for creating a book. Uses Django form for validation and sanitization;
    CSRF token is in template (form_example.html). No raw SQL.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
