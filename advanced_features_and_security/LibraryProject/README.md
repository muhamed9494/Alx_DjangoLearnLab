# Bookshelf App - Permissions and Groups Setup

This README explains the setup for managing access control in the `bookshelf` app using custom permissions and groups. It demonstrates how to restrict access to various parts of the app based on user roles, enhancing the security and functionality of the application.

## Step 1: Custom Permissions

In the `Book` model, we added custom permissions to control access to different actions. These permissions are defined within the `Meta` class of the model. The following permissions were added:

- **can_view_book**: Permission to view a book.
- **can_create_book**: Permission to create a book.
- **can_edit_book**: Permission to edit an existing book.
- **can_delete_book**: Permission to delete a book.

### Example:
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]
These permissions can be assigned to users through groups, which we'll configure in the next step.

Step 2: Groups Setup
Django allows us to define groups, each with its own set of permissions. The following groups were set up for the bookshelf app:

Editors: Users who can create and edit books. They are assigned the can_create_book and can_edit_book permissions.
Viewers: Users who can only view books. They are assigned the can_view_book permission.
Admins: Users who have full access. They can create, edit, delete, and view books, so they are assigned all permissions.
Creating and Assigning Groups:
Go to the Django admin interface at /admin/.
Under the Auth section, find and select Groups.
Create the groups (Editors, Viewers, Admins) and assign the appropriate permissions.
For example, to assign permissions to the Editors group:

Go to the Editors group.
Under the Permissions section, select can_create_book and can_edit_book.
Save the group.
Assigning Users to Groups:
Go to the Users section in the Django admin.
Select the user you want to assign to a group.
In the Groups field, add the user to one of the groups (Editors, Viewers, Admins).
Save the user.
Step 3: Enforcing Permissions in Views
To enforce permissions in views, we use the @permission_required decorator. This decorator checks if the user has the required permission before allowing them to access a view.

Here are examples of how the permissions are enforced in the views:

python
Copy code
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_create_book', raise_exception=True)
def add_book(request):
    # Only users with 'can_create_book' permission can access this view.
    # Logic for adding a book
    pass

@permission_required('bookshelf.can_edit_book', raise_exception=True)
def edit_book(request, pk):
    # Only users with 'can_edit_book' permission can access this view.
    # Logic for editing a book
    pass

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    # Only users with 'can_delete_book' permission can access this view.
    # Logic for deleting a book
    pass
Explanation:
The @permission_required decorator checks if the user has the required permission (e.g., can_create_book, can_edit_book, etc.).
If the user doesn't have the permission, they are redirected to a permission error page (or another page if you specify it).
If the user has the permission, they can access the corresponding view and perform the desired action.
Step 4: Testing Permissions
Create test users via the Django admin and assign them to different groups (Editors, Viewers, Admins).
Log in as each user and attempt to access different parts of the application:
Users in the Editors group should be able to create and edit books.
Users in the Viewers group should only be able to view books.
Users in the Admins group should have full access to create, edit, delete, and view books.
Make sure that permissions are enforced correctly by trying to perform actions that the user is not permitted to do.

Conclusion
This setup ensures that access to different actions (viewing, creating, editing, deleting) is properly managed based on the user's permissions. By using custom permissions and assigning them to groups, you can control what users are able to do within the bookshelf app.