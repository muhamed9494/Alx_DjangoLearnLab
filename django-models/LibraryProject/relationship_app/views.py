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
class AdminView(TemplateView):
    template_name = 'admin_view.html'

    @user_passes_test(lambda user: user.role == 'Admin')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# Librarian View (access for Librarian users only)
class LibrarianView(TemplateView):
    template_name = 'librarian_view.html'

    @user_passes_test(lambda user: user.role == 'Librarian')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# Member View (access for Member users only)
class MemberView(TemplateView):
    template_name = 'member_view.html'

    @user_passes_test(lambda user: user.role == 'Member')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


