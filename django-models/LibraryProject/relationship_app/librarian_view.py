# librarian_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Check if the user is a Librarian
@user_passes_test(lambda user: user.role == 'Librarian')
def librarian_view(request):
    return render(request, 'librarian_view.html')
