from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login



def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'    


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Using UserCreationForm
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()  # Show empty form for GET requests
    
    return render(request, 'register.html', {'form': form}

