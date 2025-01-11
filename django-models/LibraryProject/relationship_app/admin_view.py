# views/admin_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Define a function to check if the user has the Admin role
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

@login_required
@user_passes_test(is_admin, login_url='/login/')  # Only admin users can access this view
def admin_view(request):
    return render(request, 'roles/admin_view.html', {'message': 'Welcome, Admin!'})
