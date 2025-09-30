from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser
from django import forms


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password1', 'password2')


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not CustomUser.objects.filter(email=email).exists():
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
