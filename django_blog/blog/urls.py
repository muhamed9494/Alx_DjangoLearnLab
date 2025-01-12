from django.urls import path
from .views import RegisterView, profile_view
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='new-comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='update-comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),
]
