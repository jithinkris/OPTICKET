from django.shortcuts import render, redirect
from django.http import JsonResponse
from Admin.models import *
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.hashers import check_password

from django.views.decorators.csrf import csrf_exempt


def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        address = data.get('address')
        password = make_password(data.get('password'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')

        user = User.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )

        return JsonResponse({'message': 'Registration successful'})

    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')

        if user_type == 'Admin':
            try:
                user = AdminUser.objects.get(username=username)
                if password==user.password:
                    request.session['adin_username'] = user.username
                    return JsonResponse({'message': 'Login successful', 'user_type': 'Admin'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except Admin.DoesNotExist:
                return JsonResponse({'message': 'Admin not found'})
        
        elif user_type == 'Sub Admin':
            try:
                user = Doctor.objects.get(user_id=username)
                if password==user.password:
                    request.session['username'] = user.user_id
                    return JsonResponse({'message': 'Login successful', 'user_type': 'Sub Admin'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except Doctor.DoesNotExist:
                return JsonResponse({'message': 'Sub Admin not found'})

        elif user_type == 'User':
            try:
                user = User.objects.get(username=username)
                if password==user.password:
                    request.session['username'] = user.username
                    return JsonResponse({'message': 'Login successful', 'user_type': 'User'})
                else:
                    return JsonResponse({'message': 'Invalid password'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found'})

        return JsonResponse({'message': 'Invalid user type'})

    return render(request, 'login.html')

