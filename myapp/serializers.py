from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class LoginSerializer(serializers.ModelSerializer):
    email =serializers.EmailField(max_length = 225)
    class Meta:
        model = User
        fields = ['email','password']



class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['name','email']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['name','email','clinic_name','gender','specialty','address','profile']



class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['name','email']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['name','email','gender','address','profile']


class DoctorAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_availability
        fields = ['doctor','week','start_time','end_time']




class BookAppoinmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appoinment
        fields = ['id','doctor','date','start_time','end_time','description']
    

class SetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appoinment
        fields = ['status']
    
    