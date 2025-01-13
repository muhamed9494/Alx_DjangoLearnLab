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
from django.views.generic import TemplateView




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

# Admin View (access for Admin users only)
def admin_view(request):
    # Check if the user has the 'Admin' role
    if request.user.role != 'Admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'admin_view.html')

# Librarian View (access for Librarian users only)
def librarian_view(request):
    # Check if the user has the 'Librarian' role
    if request.user.role != 'Librarian':
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'librarian_view.html')

# Member View (access for Member users only)
def member_view(request):
    # Check if the user has the 'Member' role
    if request.user.role != 'Member':
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'member_view.html'))


