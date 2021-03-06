from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import ToDo


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

@login_required
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

@login_required
def createtodo(request):
    if request.method == 'GET':
        form = TodoForm()
        context = {'create_form': form}
        return render(request, 'todo/createtodo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('todo:currenttodos')
        except ValueError:
            form = TodoForm()
            context = {'create_form': form, 'error': 'Bad data passed in. Try again.'}
            return render(request, 'todo/createtodo.html', context)

@login_required
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, datecomleted__isnull=True).order_by('created')
    context = {'todos': todos}
    return render(request, 'todo/currenttodos.html', context)

@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, datecomleted__isnull=False).order_by('-datecomleted')
    context = {'todos': todos}
    return render(request, 'todo/completedtodos.html', context)

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {'todo': todo, 'form_red': form}
        return render(request, 'todo/viewtodo.html', context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('todo:currenttodos')
        except ValueError:
            context = {'todo': todo, 'form_red': form, 'error': 'Bad info'}
            return render(request, 'todo/viewtodo.html', context)

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecomleted = timezone.now()
        todo.save()
        return redirect('todo:currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo:currenttodos')
