from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    """Home page for Learning Log app"""
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'todo/signupuser.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todo:currenttodos')
            except IntegrityError:
                form = UserCreationForm()
                context = {'form': form, 'error': 'That username already used'}
                return render(request, 'todo/signupuser.html', context)

        else:
            form = UserCreationForm()
            context = {'form': form, 'error': 'Passwords did not match'}
            return render(request, 'todo/signupuser.html', context)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('todo:home')


def loginuser(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'todo/loginuser.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            form = AuthenticationForm()
            context = {'form': form, 'error': 'Username and password did not match'}
            return render(request, 'todo/loginuser.html', context)
        else:
            login(request, user)
            return redirect('todo:currenttodos')


def currenttodos(request):
    context = {}
    return render(request, 'todo/currenttodos.html', context)
