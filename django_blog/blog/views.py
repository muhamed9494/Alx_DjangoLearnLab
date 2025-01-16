from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from django.db.models import Q
from taggit.models import Tag





class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Profile not found")
    if request.method == 'POST':
        bio = request.POST.get('bio', profile.bio)
        profile.bio = bio
        profile.save()
        return redirect('profile')
    return render(request, 'blog/profile.html', {'profile': profile})


def home(request):
    return render(request, 'blog/home.html')	

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})   

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Display comments for a post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post-detail', pk=post.pk)
        else:
            return redirect('login')

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

# Edit comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
        
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['post_pk']})

def search_posts(request):
    form = SearchForm(request.GET)
    query = None
    results = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.objects.filter(title__icontains=query)
    
    return render(request, 'blog/search_results.html', {
        'form': form,
        'query': query,
        'results': results,
    })


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'  # Create this template
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')  # Get the slug from URL
        tag = Tag.objects.get(slug=tag_slug)  # Get the tag object
        return Post.objects.filter(tags=tag)  # Filter posts by tag

def search(request):
    query = request.GET.get('q', '')  # Get the search query from the request

    # Filter posts by tag name (case-insensitive) or content (case-insensitive)
    posts = Post.objects.filter(
        Q(tags__name__icontains=query) | Q(content__icontains=query)
    )

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})
    






