from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AdminUser)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(PatientBooking)
admin.site.register(Consultation)
admin.site.register(Feedback)
admin.site.register(TokenNumber)
admin.site.register(DailyHealthData)
