from django.urls import path
from blog.views import *
from django.contrib.auth import views as auth_views

# urls.py
urlpatterns = [
    path("startmarket",startmarket,name='startmarket'),
    path("whatsapp",whatsapp,name='whatsapp'),
    path("email",email,name='email'),
]
