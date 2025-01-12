# Blog Application Documentation

This document outlines the CRUD operations for posts and the permissions and security aspects associated with them.

## CRUD Operations for Posts

### 1. **Create a Post**
To create a new post, a user must be logged in. A user can create a post by filling out the form with a title and content. The post will be saved with the logged-in user as the author.

- **Endpoint**: `/posts/new/`
- **Method**: `POST`
- **Fields**:
  - `title`: The title of the post.
  - `content`: The content of the post.
  
**Permissions**: 
- Only authenticated users can create a post.
- The author of the post is automatically set to the logged-in user.

### 2. **Read a Post**
To read a post, users can view the details of a single post. The post is displayed with the title, content, and author information.

- **Endpoint**: `/posts/<int:pk>/`
- **Method**: `GET`
- **URL Parameter**:
  - `pk`: The ID of the post to display.

**Permissions**:
- This operation is publicly accessible, meaning anyone can read a post, regardless of whether they are logged in.

### 3. **Update a Post**
To update an existing post, the logged-in user can modify the title or content of the post. Only the author of the post can update it.

- **Endpoint**: `/posts/<int:pk>/edit/`
- **Method**: `POST`
- **Fields**:
  - `title`: The new title of the post.
  - `content`: The new content of the post.
  
**Permissions**:
- Only the author of the post can update the post.
- If the user is not the author, they will be redirected and denied access.

### 4. **Delete a Post**
To delete a post, the user must be the author of the post. Once deleted, the post will no longer be available.

- **Endpoint**: `/posts/<int:pk>/delete/`
- **Method**: `POST` (typically a `POST` for confirmation)
- **URL Parameter**:
  - `pk`: The ID of the post to delete.

**Permissions**:
- Only the author of the post can delete it.
- If the user is not the author, they will be redirected and denied access.

## Permissions and Security Aspects

### Authentication and Authorization
- **Authentication**: Users must be logged in to perform CRUD operations (except reading posts). The `LoginRequiredMixin` is used to enforce authentication on `Create`, `Update`, and `Delete` views.
  
- **Authorization**:
  - **Create**: Any logged-in user can create a post. The author is automatically set to the logged-in user.
  - **Update**: Only the author of the post can update it. This is enforced by checking whether the logged-in user is the author of the post in the `PostUpdateView`.
  - **Delete**: Only the author of the post can delete it. This is enforced by checking whether the logged-in user is the author of the post in the `PostDeleteView`.
  
  Both `Update` and `Delete` actions use the `UserPassesTestMixin` to ensure that the current user is authorized to perform the action on the post.

### CSRF Protection
- Django's built-in CSRF protection is enabled by default for all forms. This ensures that any form submission is secure and prevents Cross-Site Request Forgery (CSRF) attacks.

### Access Control
- **Post Update and Delete Views**: These views use `UserPassesTestMixin` to restrict access to the owner of the post. If an unauthorized user attempts to access these views, they will be redirected to a different page.

```python
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

How to Use
Run the server: python manage.py runserver
Access the application: Visit http://127.0.0.1:8000/ in your browser.
Create a new post: Visit /posts/new/, fill out the form, and submit.
Update a post: Navigate to the post detail page, and click the "Edit" button.
Delete a post: Navigate to the post detail page, and click the "Delete" button.
Ensure that you are logged in to perform the update or delete actions. Non-authenticated users will be redirected to the login page.


This documentation explains the CRUD operations for posts and the security measures in place to ensure only authorized users can perform certain actions.


