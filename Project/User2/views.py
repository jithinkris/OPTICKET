from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from Admin.models import *
from django.contrib.auth.hashers import make_password
import json
from django.views.decorators.csrf import csrf_exempt

def userdetls(request):
    username = request.session.get('username')
    ob=Doctor.objects.get(user_id=username)
    return ob


def doctor_home(request):
    return render(request, 'Doctor/home.html',{'name':userdetls(request).name})



from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

def doctor_view_bookings(request):
    doctor = userdetls(request)
    today = now().date()
    bookings = PatientBooking.objects.filter(doctor=doctor, appointment_date=today)

    ##### send notification to first patient

    first=bookings.first()
    if first:
        if first.status==0:
            email=first.patient.email

        # send mail notification to first person






    print("jjjjjjjjjjjjjjjj")
    print()
    return render(request, 'Doctor/view_bookings.html', {'bookings': bookings})



from django.shortcuts import render, get_object_or_404, redirect

def add_consultation(request, booking_id):
    patient_booking = get_object_or_404(PatientBooking, id=booking_id)
    patient = patient_booking.patient
    doctor = patient_booking.doctor
    appointment_date = patient_booking.appointment_date

    tk = TokenNumber.objects.filter(doctor=doctor, appointment_date=appointment_date, status=1).first()

    if tk:
        tk.ConsltNumber = patient_booking.ConsltNumber
        tk.save()
    else:
        tk = TokenNumber.objects.create(doctor=doctor, appointment_date=appointment_date, status=1, ConsltNumber=1)

    health_records = DailyHealthData.objects.filter(user=patient).order_by('-date')[:7]

    if request.method == "POST":
        symptoms = request.POST.get('symptoms')
        disease_identified = request.POST.get('disease_identified')
        remarks = request.POST.get('remarks')
        medicines = request.POST.get('medicines')

        Consultation.objects.create(
            patient_booking=patient_booking,
            symptoms=symptoms,
            disease_identified=disease_identified,
            remarks=remarks,
            medicines=medicines
        )

        patient_booking.status = 1
        patient_booking.save()

        return redirect('User2:doctor_view_bookings')  # Redirect after submission

    return render(request, 'Doctor/add_consultation.html', {
        'patient_booking': patient_booking,
        'health_records': health_records,
        'current_token': tk.ConsltNumber
    })

def stop_consultation(request):
    if request.method == "POST":
        doctor = userdetls(request)
        today = now().date()
        TokenNumber.objects.filter(doctor=doctor, status=1,appointment_date=today).update(status=0)
        return redirect('User2:doctor_home')

    return redirect('User2:doctor_home')



def doctor_profile(request):
    doctor = userdetls(request)   # Assuming `user_id` links Doctor to User
    return render(request, 'Doctor/doctor_profile.html', {'doctor': doctor})



