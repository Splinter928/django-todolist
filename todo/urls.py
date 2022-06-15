from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signupuser, name='signupuser'),  # Registration page
    path('current/', views.currenttodos, name='currenttodos'),  # ToDos page
]
