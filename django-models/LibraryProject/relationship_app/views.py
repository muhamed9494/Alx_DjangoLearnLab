from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test




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


# Views for each role
@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return render(request, 'roles/admin_view.html', {'message': 'Welcome, Admin!'})

@login_required
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    return render(request, 'roles/librarian_view.html', {'message': 'Welcome, Librarian!'})

@login_required
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    return render(request, 'roles/member_view.html', {'message': 'Welcome, Member!'})

# Role-checking functions
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


