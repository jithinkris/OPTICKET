from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def admin_home(request):
    return render(request, 'Admin/home.html')

def view_all_users(request):
    users = User.objects.all()
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
            return JsonResponse({'message': 'User blocked successfully'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'})
    return render(request, 'Admin/admin_viewusers.html', {'users': users})

@csrf_exempt
def add_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        specialization = data.get('specialization')
        phone = data.get('phone')
        email = data.get('email')
        experience = data.get('experience')
        user_id = data.get('user_id')
        password = data.get('password')

        # Check if all fields are filled
        if name and specialization and phone and email and experience and user_id and password:
            # Check if the user_id is unique
            if Doctor.objects.filter(user_id=user_id).exists():
                return JsonResponse({'message': 'User ID already taken. Choose another one.'}, status=400)

            doctor = Doctor(
                name=name,
                specialization=specialization,
                phone=phone,
                email=email,
                experience=experience,
                user_id=user_id,
                password=password  # Storing as plain text (not recommended for production)
            )
            doctor.save()
            return JsonResponse({'message': 'Doctor added successfully'}, status=201)
        else:
            return JsonResponse({'message': 'All fields are required'}, status=400)

    return render(request, 'Admin/add_doctor.html')


# View Doctors
def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'Admin/view_doctors.html', {'doctors': doctors})


def view_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'Admin/feedback.html', {'feedbacks': feedbacks})


from datetime import date
def admin_view_bookings(request):
    selected_date = request.GET.get('date', str(date.today()))
    bookings = PatientBooking.objects.filter(appointment_date=selected_date).order_by('doctor__name', 'time')

    doctors = Doctor.objects.all()

    context = {
        'bookings': bookings,
        'selected_date': selected_date,
        'doctors': doctors
    }
    return render(request, 'Admin/bookings.html', context)


def admin_view_payments(request):
    bookings = PatientBooking.objects.all().order_by('-appointment_date')
    cost_per_booking = 500
    total_revenue = bookings.count() * cost_per_booking

    context = {
        'bookings': bookings,
        'cost_per_booking': cost_per_booking,
        'total_revenue': total_revenue
    }
    return render(request, 'payments.html', context)



def admin_view_tokens(request):
    selected_date = request.GET.get('date', str(date.today()))  # Default to today’s date
    doctors = Doctor.objects.all()

    doctor_tokens = {}
    for doctor in doctors:
        current_token = TokenNumber.objects.filter(doctor=doctor, appointment_date=selected_date, status=1).order_by('-ConsltNumber').first()
        waiting_tokens = TokenNumber.objects.filter(doctor=doctor, appointment_date=selected_date, status=0).order_by('ConsltNumber')

        doctor_tokens[doctor] = {
            'current_token': current_token.ConsltNumber if current_token else "N/A",
            'waiting_tokens': [token.ConsltNumber for token in waiting_tokens]
        }

    context = {
        'doctor_tokens': doctor_tokens,
        'selected_date': selected_date
    }
    return render(request, 'Admin/tokens.html', context)


