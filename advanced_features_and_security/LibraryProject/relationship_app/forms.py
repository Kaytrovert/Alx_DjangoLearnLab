"""
Django forms for relationship_app. Validate and sanitize user input;
use with ORM (no raw SQL) to prevent SQL injection and invalid data.
"""

from django import forms
from .models import Book, Author


class BookForm(forms.ModelForm):
    """Form for creating/editing Book. Validates title and author_id (no raw SQL)."""

    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 200}),
        }
