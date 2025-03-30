from rest_framework import serializers
from Admin.models import User,Feedback,DailyHealthData,Doctor

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','phone_number','address','password','first_name','last_name','date_of_birth']

class UserRegSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number','address','password','first_name','last_name','date_of_birth']


class DailyHealthDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Accept email in input

    class Meta:
        model = DailyHealthData
        fields = [
            'email', 'date', 'systolic_bp', 'diastolic_bp', 'pulse',
            'blood_sugar_fasting', 'blood_sugar_post_meal', 'notes'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.filter(email=email).first()  # Get user instance if exists

        return DailyHealthData.objects.create(user=user, **validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'phone', 'email', 'experience', 'date_joined']
