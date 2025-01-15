from django.shortcuts import render
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden




def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'

    
def check_role(role):
    def decorator(user):
        return user.is_authenticated and user.profile.role == role
    return decorator

@user_passes_test(check_role('Admin'), login_url='/accounts/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(check_role('Librarian'), login_url='/accounts/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(check_role('Member'), login_url='/accounts/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'role': 'Member'})


