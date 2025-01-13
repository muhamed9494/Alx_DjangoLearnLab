# member_view.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Check if the user is a Member
@user_passes_test(lambda user: user.role == 'Member')
def member_view(request):
    return render(request, 'member_view.html')
