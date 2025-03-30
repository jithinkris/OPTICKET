from django.contrib import admin
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from Admin.models import *
from User.serializer import *
from django.shortcuts import get_object_or_404


import random
@api_view(['POST'])
def book_appointment(request):
    try:
        patient_email = request.data.get('email')
        doctor_email = request.data.get('doctor')
        appointment_date = request.data.get('appointment_date')
        symptoms = request.data.get('symptoms', '')
        additional_details = request.data.get('additional_details', '')

        if not (patient_email and doctor_email and appointment_date):
            return Response({'error': 'Missing required fields'}, status=400)

        patient = get_object_or_404(User, email=patient_email)
        doctor = get_object_or_404(Doctor, email=doctor_email)

        last_booking = PatientBooking.objects.filter(
            doctor=doctor, appointment_date=appointment_date
        ).order_by('-ConsltNumber').first()

        next_consult_number = last_booking.ConsltNumber + 1 if last_booking else 1

        # Calculate appointment time (starting from 9 AM)
        hours = 9 + ((next_consult_number - 1) * 10) // 60
        minutes = ((next_consult_number - 1) * 10) % 60

        # Add a random delay of 0-7 minutes
        minutes += random.randint(0, 7)

        # Adjust hours if minutes exceed 60
        if minutes >= 60:
            hours += 1
            minutes -= 60

        predicted_time = f"{hours}:{minutes:02d} AM"

        # Create appointment entry
        appointment = PatientBooking.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            time=predicted_time,
            symptoms=symptoms,
            additional_details=additional_details,
            ConsltNumber=next_consult_number
        )

        return Response({
            'message': 'Appointment booked successfully!',
            'appointment_id': appointment.id,
            'opticket_number': appointment.opticket_number,
            'time': appointment.time,
            'ConsltNumber': appointment.ConsltNumber
        }, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=400)
