# 🔐 Built-in Authentication Views in Django

Django provides several **class-based views** in `django.contrib.auth.views` to handle common authentication actions like login, logout, password change, and password reset — all customizable and production-ready.

📚 **Import path:**

```python
from django.contrib.auth import views as auth_views
```

---

## 🧾 1. LoginView

Handles user login.

```python
# urls.py
path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
```

### Options:

* `template_name`: Template to render the form.
* `authentication_form`: Custom login form.
* `redirect_authenticated_user`: Redirect logged-in users automatically.

### Default template: `registration/login.html`

---

## 🚪 2. LogoutView

Handles user logout.

```python
path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
```

### Options:

* `next_page`: Where to redirect after logout.
* Or set `LOGOUT_REDIRECT_URL` in `settings.py`.

---

## 🔑 3. PasswordChangeView

Allows logged-in users to change their password.

```python
path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
```

### Required templates:

* `password_change_form.html`
* `password_change_done.html`

### Notes:

* Requires user to be logged in.
* Redirects to success URL after password change.

---

## 🔐 4. PasswordResetView (Email-based Reset)

Initiates the password reset process by sending an email.

```python
path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
```

### Required templates:

* `password_reset_form.html` — form to enter email
* `password_reset_done.html` — confirmation

---

## 📬 5. PasswordResetConfirmView

This view is linked from the email users receive.

```python
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
```

### Required templates:

* `password_reset_confirm.html` — form for new password
* `password_reset_complete.html` — success message

---

## 🧩 Default Template Directory Structure

Django expects your templates to be located like this:

```
templates/
└── registration/
    ├── login.html
    ├── password_change_form.html
    ├── password_change_done.html
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    ├── password_reset_complete.html
```

### 🔖 Example Templates

#### `login.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
<a href="{% url 'password_reset' %}">Forgot password?</a>
{% endblock %}
```

#### `password_change_form.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Change Password</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Change</button>
</form>
{% endblock %}
```

#### `password_change_done.html`

```html
{% extends "base.html" %}
{% block content %}
<p>Your password has been changed successfully.</p>
<a href="{% url 'home' %}">Return to home</a>
{% endblock %}
```

#### `password_reset_form.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Reset Password</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Send reset link</button>
</form>
{% endblock %}
```

#### `password_reset_done.html`

```html
{% extends "base.html" %}
{% block content %}
<p>We’ve emailed you instructions for setting your password. Please check your inbox.</p>
{% endblock %}
```

#### `password_reset_confirm.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Set New Password</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Reset password</button>
</form>
{% endblock %}
```

#### `password_reset_complete.html`

```html
{% extends "base.html" %}
{% block content %}
<p>Your password has been reset successfully. You can now <a href="{% url 'login' %}">log in</a>.</p>
{% endblock %}
```

---

## ⚙️ Settings (Optional Enhancements)

```python
# settings.py
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```

---

## 🧠 Summary Table

| View                        | URL Name                  | Purpose                                 |
| --------------------------- | ------------------------- | --------------------------------------- |
| `LoginView`                 | `login`                   | Logs the user in                        |
| `LogoutView`                | `logout`                  | Logs the user out                       |
| `PasswordChangeView`        | `password_change`         | Lets users change password              |
| `PasswordChangeDoneView`    | `password_change_done`    | Confirms password was changed           |
| `PasswordResetView`         | `password_reset`          | Starts password reset (email)           |
| `PasswordResetDoneView`     | `password_reset_done`     | Confirms email was sent                 |
| `PasswordResetConfirmView`  | `password_reset_confirm`  | Confirms reset link & sets new password |
| `PasswordResetCompleteView` | `password_reset_complete` | Password has been reset                 |
