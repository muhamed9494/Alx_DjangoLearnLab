from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test



def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'    


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login after successful registration
    template_name = 'registration/register.html'

# Helper functions to check roles
def is_admin(user):
    return user.is_authenticated and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.profile.role == 'Member'
    
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html', {'message': 'Welcome, Admin!'})

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html', {'message': 'Welcome, Librarian!'})

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html', {'message': 'Welcome, Member!'})


