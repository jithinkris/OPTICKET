from .views import *
from django.urls import path

app_name="Guest"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),


]
