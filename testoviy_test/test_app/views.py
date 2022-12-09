from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"


def logout_user(request):
    logout(request)
    return redirect("login")