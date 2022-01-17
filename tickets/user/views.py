from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm


@login_required
def index(request):
    return redirect('profile')


def sign_in(request):
    if request.method == "GET":
        return render(request, 'sign_in.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.info(request, 'The username or password does not match.')
            return render(request, 'sign_in.html')
        return redirect('tickets')


def sign_up(request):
    user_form = CreateUserForm()

    if request.method == "GET":
        content = {
            'user_form': user_form
        }
        return render(request, 'sign_up.html', content)

    elif request.method == "POST":
        user_form = CreateUserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = request.POST['email']
            user.save()

            login(request, user)
            return redirect('tickets')

        else:
            content = {
                'user_form': user_form
            }
            return render(request, 'sign_up.html', content)


@login_required
def profile(request):
    return render(request, 'profile.html')


def logout_user(request):
    logout(request)
    return redirect('index')
