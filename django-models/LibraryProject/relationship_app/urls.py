from django.urls import path
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view: Library detail view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
