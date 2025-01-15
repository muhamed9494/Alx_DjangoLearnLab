from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from django.views.generic import TemplateView


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('signup/', SignUpView.as_view(), name='register'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),


]
