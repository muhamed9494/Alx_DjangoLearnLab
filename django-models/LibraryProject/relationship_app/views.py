from django.shortcuts import render, get_object_or_404
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import permission_required




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



@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        
        Book.objects.create(title=title, author=author, description=description)
        return redirect('list_books')  # Redirect to book list

    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.description = request.POST.get('description', book.description)
        
        book.save()
        return redirect('list_books')  # Redirect to book list

    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')  # Redirect to book list
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})
