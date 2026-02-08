"""
Django forms for bookshelf app.
Use forms to validate and sanitize user input; avoids SQL injection and invalid data.
"""

from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating/editing Book. Validates and sanitizes input (no raw SQL)."""

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 200}),
            'author': forms.TextInput(attrs={'maxlength': 100}),
            'publication_year': forms.NumberInput(attrs={'min': 1, 'max': 2100}),
        }


class BookSearchForm(forms.Form):
    """Safe search: use form validation and ORM filter (parameterized), never string-format SQL."""

    query = forms.CharField(max_length=200, required=False, strip=True)
