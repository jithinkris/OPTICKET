from django.urls import path
from .views import *

app_name="Admin"


urlpatterns = [
 path('admin_home',admin_home, name='admin_home'),
 path('view_users/', view_all_users, name='view_all_users'),
 path('add_doctor/', add_doctor, name='add_doctor'),
 path('view_doctors/',view_doctors, name='view_doctors'),
 path('view_feedback/',view_feedback, name='view_feedback'),
 path('admin/bookings/', admin_view_bookings, name='admin_view_bookings'),
 path('admin/payments/', admin_view_payments, name='admin_view_payments'),
 path('admin_view_tokens/', admin_view_tokens, name='admin_view_tokens'),

]

