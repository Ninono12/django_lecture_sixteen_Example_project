from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView
from user.forms import UserRegistrationForm
from user.models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


@method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url='login'), name='dispatch')
class UserRegisterView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'user_register.html'
    success_url = reverse_lazy('login')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('class_blog_post_list')
        messages.error(request, "Invalid username or password.")
        return render(request, self.template_name, context={'form': form})


class LogoutView(View):

    def get(self, request):
        auth_logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')
