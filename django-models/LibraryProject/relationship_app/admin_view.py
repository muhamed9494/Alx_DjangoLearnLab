from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.profile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html', {'role': 'Admin'})
