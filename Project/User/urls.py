from django.urls import path
from User2 import admin as v1
from .views import *

app_name="User"


urlpatterns = [
    path('UserReg',UserReg,name='UserReg'),
    path('UserLogin',UserLogin,name='UserLogin'),
    path('UserProfile',UserProfile,name='UserProfile'),
    path('submit-feedback', submit_feedback, name='submit-feedback'),
    path('submit-health-data', submit_health_data, name='submit-health-data'),
    path('doctors', view_doctors, name='view-doctors'),
    path('book_appointment', v1.book_appointment, name='book_appointment'),
    path('view_my_bookings', view_my_bookings, name='view_my_bookings'),
    path('view_my_bookings_current', view_my_bookings_current, name='view_my_bookings_current'),
    path('view_prescription', view_prescription, name='view_prescription'),


]
