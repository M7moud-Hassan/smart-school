from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from authentications.forms import LoginForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authentications/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            branch = form.cleaned_data.get('branches')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.branch != branch:
                    messages.error(request, 'you not include in this branch')
                else:
                    login(request, user)
                    return redirect("/")
            else:
                messages.error(request, 'may be password/email not correct')
        else:
            messages.error(request, 'check inputs')
        return render(request, 'authentications/login.html', context={'form': form})
