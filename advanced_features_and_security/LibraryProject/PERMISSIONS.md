# Permissions and Groups Setup

This document describes how permissions and groups are configured and used in the application.

## Custom Permissions (Model: Book)

The `relationship_app.Book` model defines four custom permissions in its `Meta.permissions`:

| Permission   | Codename    | Description    |
|-------------|-------------|----------------|
| Can view    | `can_view`  | View book list and library details |
| Can create  | `can_create`| Add new books  |
| Can edit    | `can_edit`  | Edit existing books |
| Can delete  | `can_delete`| Delete books   |

These are defined in `relationship_app/models.py` on the `Book` model.

## Groups and Assigned Permissions

Three groups are created (via migration `0004_create_groups`) and can be managed in Django Admin under **Auth > Groups**:

| Group    | Permissions assigned                          |
|----------|------------------------------------------------|
| Viewers  | `can_view` only                               |
| Editors  | `can_view`, `can_create`, `can_edit`          |
| Admins   | `can_view`, `can_create`, `can_edit`, `can_delete` |

- **Viewers**: Can only view the book list and library details.
- **Editors**: Can view, create, and edit books (no delete).
- **Admins**: Full access (view, create, edit, delete).

## Enforcing Permissions in Views

Views are protected with `@permission_required` (and `PermissionRequiredMixin` for class-based views):

| View           | Permission required | Decorator / Mixin           |
|----------------|---------------------|-----------------------------|
| `list_books`   | `relationship_app.can_view`   | `@permission_required`      |
| `LibraryDetailView` | `relationship_app.can_view`   | `PermissionRequiredMixin`   |
| `add_book`     | `relationship_app.can_create` | `@permission_required`      |
| `edit_book`    | `relationship_app.can_edit`   | `@permission_required`      |
| `delete_book`  | `relationship_app.can_delete`| `@permission_required`      |

Example in code:

```python
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
```

Users without the required permission receive **403 Forbidden** (`raise_exception=True`).

## How to Test

1. Run migrations so groups exist: `python manage.py migrate`
2. In Django Admin, create users and assign them to **Viewers**, **Editors**, or **Admins**.
3. Log in as each user and visit:
   - `/books/` – requires `can_view`
   - `/add_book/` – requires `can_create`
   - Edit/delete links – require `can_edit` / `can_delete`
4. Confirm that users can only access views allowed by their group’s permissions.
