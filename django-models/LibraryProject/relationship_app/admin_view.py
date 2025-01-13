# admin_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Check if the user is an Admin
@user_passes_test(lambda user: user.role == 'Admin')
def admin_view(request):
    return render(request, 'admin_view.html')
