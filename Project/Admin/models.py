from django.db import models

# Create your models here.
class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)
    def __str__(self):
        return self.username


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.CharField(max_length=30,blank=True, null=True)
    deviceid = models.CharField(max_length=550, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    experience = models.PositiveIntegerField()  # In years
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class PatientBooking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateField()
    time=models.CharField(max_length=100,blank=True,null=True) # predicted
    symptoms = models.TextField()
    additional_details = models.TextField(blank=True, null=True)
    ConsltNumber=models.IntegerField(default=0)
    opticket_number = models.PositiveIntegerField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.opticket_number:
            last_ticket = PatientBooking.objects.order_by('-opticket_number').first()
            self.opticket_number = last_ticket.opticket_number + 1 if last_ticket else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} -> Dr. {self.doctor.name} on {self.appointment_date} (Ticket #{self.opticket_number})"



class Consultation(models.Model):
    patient_booking = models.ForeignKey('PatientBooking', on_delete=models.CASCADE, related_name="consultations")
    symptoms = models.TextField()
    disease_identified = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    medicines = models.TextField(help_text="List of prescribed medicines")
    consultation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation for {self.patient_booking.patient.username} on {self.consultation_date}"


class Feedback(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.CharField(max_length=150, unique=True)



class TokenNumber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    status=models.IntegerField(default=1)
    ConsltNumber=models.IntegerField(default=0)



from datetime import date

class DailyHealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)  # Stores the date of the entry
    systolic_bp = models.IntegerField(null=True, blank=True)  # Upper BP value
    diastolic_bp = models.IntegerField(null=True, blank=True)  # Lower BP value
    pulse = models.IntegerField(null=True, blank=True)  # Heart rate
    blood_sugar_fasting = models.FloatField(null=True, blank=True)  # Fasting sugar level
    blood_sugar_post_meal = models.FloatField(null=True, blank=True)  # Post-meal sugar level
    notes = models.TextField(null=True, blank=True)  # Additional health notes


