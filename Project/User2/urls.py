from django.urls import path
from .views import *


app_name="User2"

urlpatterns = [
path('home/', doctor_home, name='doctor_home'),
path('doctor/bookings/', doctor_view_bookings, name='doctor_view_bookings'),
path('doctor/consult/<int:booking_id>/', add_consultation, name='consult_patient'),
path('doctor/profile/', doctor_profile, name='doctor_profile'),
path('stop-consultation/', stop_consultation, name='stop_consultation'),

]
