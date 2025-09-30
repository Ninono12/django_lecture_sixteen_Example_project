from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from blog_post import settings
from user.forms import PasswordResetRequestForm, SetNewPasswordForm

from user.models import CustomUser
from user.utils import custom_password_reset_token


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, template_name="password_reset/password_reset_request.html", context={"form": form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = CustomUser.objects.get(email=email)

            # Generate reset link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = custom_password_reset_token.make_token(user)
            reset_link = f"http://127.0.0.1:8000/user/reset/{uid}/{token}/"

            # Send email
            subject = "Password Reset Request"
            message = render_to_string(template_name="password_reset/password_reset_email.txt", context={
                "user": user,
                "reset_link": reset_link,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )

            return render(request, template_name="password_reset/password_reset_sent.html")

        return render(request, template_name="password_reset/password_reset_request.html", context={"form": form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and custom_password_reset_token.check_token(user, token):
            form = SetNewPasswordForm()
            return render(request, template_name="password_reset/password_reset_confirm.html", context={
                "form": form,
                "uidb64": uidb64,
                "token": token
            })
        else:
            return render(request, template_name="password_reset/password_reset_invalid.html")

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        form = SetNewPasswordForm(request.POST)
        if user and custom_password_reset_token.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data["new_password1"]
                user.set_password(new_password)
                user.save()
                login(request, user)  # optional
                return render(request, "password_reset/password_reset_complete.html")

        return render(request, "password_reset/password_reset_confirm.html", {
            "form": form,
            "uidb64": uidb64,
            "token": token
        })
