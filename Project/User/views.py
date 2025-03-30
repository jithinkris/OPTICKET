
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from Admin.models import *
from .serializer import *
from rest_framework import status


@api_view(['POST'])
def UserReg(request):
    if request.method == 'POST':
        data=request.data
        serializer=UserRegSerializer(data=data)
        print(serializer)
        email = data.get('email')
        username = data.get('username')
        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            return Response({"output": "0", "message": "Email already exists."}, status=status.HTTP_409_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"output": "0", "message": "username already exists."}, status=status.HTTP_409_BAD_REQUEST)


        if serializer.is_valid():
            serializer.save()
            return Response({"output": "1"},status=status.HTTP_201_CREATED)
        return Response({"output": "0"},status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def UserLogin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        deviceid=request.data.get('deviceid')
        if User.objects.filter(email=email,password=password).first() != None:
            #request.session['email']=Clint.objects.filter(email=email,password=password,status=1).first().email
            user=User.objects.filter(email=email,password=password).first()
            user.deviceid=deviceid
            user.save()
            return Response({"message": "Login successful","email":User.objects.filter(email=email,password=password).first().email,"name":User.objects.filter(email=email,password=password).first().first_name}, status=status.HTTP_200_OK)
        else:
            return Response({ "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)








@api_view(['GET','PUT'])
def UserProfile(request):
    if request.method == 'GET':
        email=request.data.get('email')
        user=User.objects.filter(email=email).first()
        serializer=UserRegSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        email=request.data.get('email')
        user=User.objects.filter(email=email).first()
        data=request.data
        serializer=UserRegSerializer1(user,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"output": "1"},status=status.HTTP_201_CREATED)
        return Response({"output": "0"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def submit_feedback(request):
    if request.method == 'POST':
        email = request.data.get('email')
        feedback= request.data.get('feedback')
        user=User.objects.filter(email=email).first()
        Feedback.objects.create(message=feedback,patient=user)
        return Response({"message": "Feedback submitted successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def submit_health_data(request):
    serializer = DailyHealthDataSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Health data submitted successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def view_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




from django.shortcuts import get_object_or_404



def predict_time(doctor_name, consult_number, symptoms):
    input_features = np.array([[hash(doctor_name) % 1000, consult_number, hash(symptoms) % 1000]])
    predicted_time_offset = model.predict(input_features)[0]

    hours = 9 + (predicted_time_offset // 60)
    minutes = predicted_time_offset % 60
    return f"{hours}:{minutes:02d} AM"

@api_view(['POST'])
def book_appointments(request):
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
        doctor_name = doctor.name

        last_booking = PatientBooking.objects.filter(
            doctor=doctor, appointment_date=appointment_date
        ).order_by('-ConsltNumber').first()

        next_consult_number = last_booking.ConsltNumber + 1 if last_booking else 1
        predicted_time = predict_time(doctor_name, next_consult_number, symptoms)

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


@api_view(['GET'])
def view_my_bookings(request):
    try:
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=400)

        patient = get_object_or_404(User, email=email)

        bookings = PatientBooking.objects.filter(patient=patient,status=1).order_by('-appointment_date')

        booking_list = [{
            'doctor': booking.doctor.name,
            'appointment_date': booking.appointment_date,
            'time': booking.time,
            'symptoms': booking.symptoms,
            'additional_details': booking.additional_details,
            'ConsltNumber': booking.ConsltNumber,
            'opticket_number': booking.opticket_number,
            'status': booking.status,
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for booking in bookings]

        return Response({'bookings': booking_list,'name':patient.first_name}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)




@api_view(['GET'])
def view_my_bookings_current(request):
    try:
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=400)

        patient = get_object_or_404(User, email=email)

        bookings = PatientBooking.objects.filter(patient=patient, status=0).order_by('-appointment_date')

        booking_list = []
        for booking in bookings:
            # Check if appointment exists in TokenNumber table
            token_entry = TokenNumber.objects.filter(
                doctor=booking.doctor,
                appointment_date=booking.appointment_date
            ).first()

            started_sts = 1 if token_entry else 0
            current_ConsltNumber = token_entry.ConsltNumber if token_entry else 0

            booking_list.append({
                'doctor': booking.doctor.name,
                'appointment_date': booking.appointment_date,
                'time': booking.time,
                'symptoms': booking.symptoms,
                'additional_details': booking.additional_details,
                'ConsltNumber': booking.ConsltNumber,
                'opticket_number': booking.opticket_number,
                'status': booking.status,
                'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'started_sts': started_sts,
                'current_ConsltNumber': current_ConsltNumber
            })

        return Response({'bookings': booking_list,'name':patient.first_name}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def view_prescription(request):
    opticket_number = request.data.get('opticket_number')

    if not opticket_number:
        return Response({"error": "opticket_number is required"}, status=400)

    try:
        patient_booking = PatientBooking.objects.get(opticket_number=opticket_number)
        consultations = Consultation.objects.filter(patient_booking=patient_booking)

        if consultations.exists():
            consultation_data = [
                {
                    "symptoms": consultation.symptoms,
                    "disease_identified": consultation.disease_identified,
                    "remarks": consultation.remarks,
                    "medicines": consultation.medicines,
                    "consultation_date": consultation.consultation_date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for consultation in consultations
            ]
            return Response(consultation_data, status=200)

        return Response({"message": "No consultations found for this ticket"}, status=404)

    except PatientBooking.DoesNotExist:
        return Response({"error": "Invalid opticket_number or unauthorized access"}, status=404)





