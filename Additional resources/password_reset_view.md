# Django Custom Password Reset Flow (With Email)

This guide shows how to implement a **custom password reset system** in Django without using the built-in views. We will build:

1. A form to request a password reset by email.  
2. A view that generates a reset token and sends an email.  
3. A view where the user sets a new password.  
4. Templates for each step.  

We will still use **Django’s security utilities** (`PasswordResetTokenGenerator`, `urlsafe_base64_encode`) to generate secure tokens.

---

## 1. Email Configuration

### Development (test mode)
Instead of sending real emails, Django prints them to the terminal:

```python
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@example.com"
````

### Production (SMTP example)

Use SMTP with environment variables:

```python
# settings.py
import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@example.com")
```

---

## 2. Token Utility

We’ll use Django’s built-in token generator, wrapped in a helper class.

```python
# utils/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

custom_password_reset_token = CustomPasswordResetTokenGenerator()
```

---

## 3. Forms

```python
# forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email.")
        return email


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        if p1 and len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return cleaned_data
```

---

## 4. Views

```python
# views.py
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from .forms import PasswordResetRequestForm, SetNewPasswordForm
from .utils.tokens import custom_password_reset_token

User = get_user_model()


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, "auth/password_reset_request.html", {"form": form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)

            # Generate reset link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = custom_password_reset_token.make_token(user)
            domain = get_current_site(request).domain
            reset_link = f"http://{domain}/reset/{uid}/{token}/"

            # Send email
            subject = "Password Reset Request"
            message = render_to_string("auth/password_reset_email.txt", {
                "user": user,
                "reset_link": reset_link,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=[email]
             )

            return render(request, "auth/password_reset_sent.html")

        return render(request, "auth/password_reset_request.html", {"form": form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and custom_password_reset_token.check_token(user, token):
            form = SetNewPasswordForm()
            return render(request, "auth/password_reset_confirm.html", {
                "form": form,
                "uidb64": uidb64,
                "token": token
            })
        else:
            return render(request, "auth/password_reset_invalid.html")

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        form = SetNewPasswordForm(request.POST)
        if user and custom_password_reset_token.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                user.set_password(new_password)
                user.save()
                login(request, user)  # optional
                return render(request, "auth/password_reset_complete.html")

        return render(request, "auth/password_reset_confirm.html", {
            "form": form,
            "uidb64": uidb64,
            "token": token
        })
```

---

## 5. URLs

```python
# urls.py
from django.urls import path
from .views import PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
```

---

## 6. Templates

### a) Request Form

```html
<!-- templates/auth/password_reset_request.html -->
<h2>Forgot Password?</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send Reset Link</button>
</form>
```

### b) Email Sent

```html
<!-- templates/auth/password_reset_sent.html -->
<h2>Check your email</h2>
<p>If the email exists, you’ll receive a password reset link.</p>
```

### c) Reset Email

```text
<!-- templates/auth/password_reset_email.txt -->
Hello {{ user.get_username }},

Click the link below to reset your password:
{{ reset_link }}

If you did not request this, ignore this email.
```

### d) Password Reset Confirm

```html
<!-- templates/auth/password_reset_confirm.html -->
<h2>Set a New Password</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Change Password</button>
</form>
```

### e) Reset Complete

```html
<!-- templates/auth/password_reset_complete.html -->
<h2>Password reset successful</h2>
<p>You can now log in with your new password.</p>
```

### f) Invalid Token

```html
<!-- templates/auth/password_reset_invalid.html -->
<h2>Invalid or expired link</h2>
<p>Please request a new password reset.</p>
```

---

## 7. Flow Summary

1. **User enters email** → `PasswordResetRequestView`
2. **App sends reset link** with UID + token via email → `password_reset_email.txt`
3. **User clicks link and sets a new password** → `PasswordResetConfirmView`
4. **Password is updated** → success page shown

Would you like me to also include a **Mermaid diagram** of this flow for the doc (good for teaching/lectures)?
```
