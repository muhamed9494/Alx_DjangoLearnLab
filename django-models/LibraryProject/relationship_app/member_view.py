# views/member_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Define a function to check if the user has the Member role
def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

@login_required
@user_passes_test(is_member, login_url='/login/')  # Only member users can access this view
def member_view(request):
    return render(request, 'roles/member_view.html', {'message': 'Welcome, Member!'})
