# views/librarian_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Define a function to check if the user has the Librarian role
def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

@login_required
@user_passes_test(is_librarian, login_url='/login/')  # Only librarian users can access this view
def librarian_view(request):
    return render(request, 'roles/librarian_view.html', {'message': 'Welcome, Librarian!'})
