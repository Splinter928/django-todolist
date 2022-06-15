from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login


def home(request):
    """Home page for Learning Log app"""
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method != 'POST':
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


def currenttodos(request):
    context = {}
    return render(request, 'todo/currenttodos.html', context)