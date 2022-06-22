from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),  # Home page

    path('signup/', views.signupuser, name='signupuser'),  # Registration page
    path('logout/', views.logoutuser, name='logoutuser'),  # Logout page
    path('login/', views.loginuser, name='loginuser'),  # Logout page

    path('create/', views.createtodo, name='createtodo'),  # ToDos create page
    path('current/', views.currenttodos, name='currenttodos'),  # ToDos page
    path('completed/', views.completedtodos, name='completedtodos'),  # Completed ToDos page
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),  # View 1 todos
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),  # Complete todos url
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),  # Delete todos url
]
