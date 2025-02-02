from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm  # Assuming you have a form for the Book model


# Enforce permissions in views
@permission_required('bookshelf.can_create_book', raise_exception=True)
def add_book(request):
    form = ExampleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_books')  # Redirect to book list
    return render(request, 'bookshelf/add_book.html', {'form': form})


@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = ExampleForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books')  # Redirect to book list
    return render(request, 'bookshelf/edit_book.html', {'form': form})


@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')  # Redirect to book list
    return render(request, 'bookshelf/delete_book.html', {'book': book})
