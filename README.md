# Django

- **Built-in authentication views** - https://docs.djangoproject.com/en/5.1/topics/auth/default/#module-django.contrib.auth.views
- **Authentication** - https://docs.djangoproject.com/en/5.2/topics/auth/default/
- **Password Reset** - https://github.com/BTU-Women-in-AI-Python-course-2025/python_lecture_16/blob/main/Additional%20resources/password_reset_view.md
- **Password Reset Token Generator** - https://github.com/django/django/blob/main/django/contrib/auth/tokens.py
  
## 📚 **Student Task: Build a Simple Authentication System with Password Reset Token**


1. **Create a new Django project or use an existing one.**

2. **Create a login view using Django's built-in authentication**  
   - Use `django.contrib.auth.views.LoginView`.
   - Configure `urls.py` to route `/login/` to this view.
   - Create a simple HTML template for login (e.g. `login.html`).

3. **Create a custom class for generating a password reset token**  
   - In a new Python file (e.g. `utils.py`), create a class that extends `PasswordResetTokenGenerator`.

   Example:
   ```python
   from django.contrib.auth.tokens import PasswordResetTokenGenerator

   class MyPasswordResetTokenGenerator(PasswordResetTokenGenerator):
       pass
   ```
