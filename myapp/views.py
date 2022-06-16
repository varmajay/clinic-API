from random import choices
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import *
from django.conf import settings
from django.core.mail import send_mail
from myapp.serializers import *
from .models import * 
from rest_framework import status
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
import jwt, json
from .utils import *
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from django.db.models import Value, DateField
# Create your views here.

# Creating Token
@api_view(['GET'])
def index(request):
    url_pattern = {
        "Login":'login/',
        "Logout":'logout/',
        "Create Doctor":'doctor-create/',
        "View Doctor":'doctor-view/',
        "Edit Doctor":'doctor-edit/id',
        "Delete Doctor":'doctor-delete/id',
        "Doctor Profile":'doctor-profile/id',
        "Create Patient":'patient-create/',
        "View Patient":'patient-view/',
        "Edit Patient":'patient-edit/id',
        "Delete Patient":'patient-delete/id',
        "Patient Profile":'patient-profile/id',
        "Add Slot":'slot-add/',
        "Update Slot":'slot-update/id',
        "Delete Slot":'slot-delete/id',
        "View Slot":'slot-view/',
        "Admin View Appoinment":'admin-appoinment/',
        "Doctor Access his Appoinment":'doctor-appoinment/',
        "Doctor Set Appoinment Status":'doctor-appoinment/id',
        "Book Appoinment":'book/',
        "Delete Book Appoinment":'book-delete/id'
        
    }
    return Response(url_pattern)


class LoginAPI(GenericAPIView):
    # permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            password = request.data['password']
            user1 = User.objects.get(email=email)
            if user1 is not None:
                try:
                    user = authenticate(request, email=user1.email, password=password)
                    if user is None:
                        return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"status": status.HTTP_400_BAD_REQUEST, 'error':True, 'message': "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
        if user:
            payload = {
                'id': user.id,
                'email': user.email,
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            UserToken.objects.create(user=user, token=jwt_token)
            return Response(data={"status": status.HTTP_200_OK,
                                "error": False,
                                "message": "User Login Successfully.",
                                    "result": {'id': user.id,
                                            'name':user.name, 
                                            'email':user.email, 
                                            'token': jwt_token,
                                            }},
                                status=status.HTTP_200_OK)



class LogoutView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        try:
            token = Authenticate(self, request)
            token1 = token.decode("utf-8")
            try:
                user_token = UserToken.objects.get(user=request.user, token=token1)
                user_token.delete()
                logout(request)
            except:
                return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                      "Message": 'Already Logged Out.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"Status": status.HTTP_200_OK,
                                  "Message": "User Logged Out."},
                            status=status.HTTP_200_OK)
        except:
            return Response(data={"Status":status.HTTP_400_BAD_REQUEST,
                                    "Message":'Already Logged Out.'},
                            status=status.HTTP_400_BAD_REQUEST)


# ------------------------------Admin Doctor CRUD------------------------------

class DoctorCreateAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DoctorCreateSerializer
    def post(self,request):
        # password = ''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        password = make_password('12345')
        serializer = DoctorCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            # subject = 'welcome to Clinic'
            # message = f"""Hello {request.data['name']},
            # Your Username is  {request.data['email']},
            # Your Password is {password} """
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [request.data['email'], ]
            # send_mail( subject, message, email_from, recipient_list )
            serializer.save(password = password,role ='doctor')
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DoctorViewAPI(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role='doctor')
    serializer_class = DoctorSerializer



class DoctorEditAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role = 'doctor')
    serializer_class = DoctorSerializer



class DoctorDeleteAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = DoctorSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')




# ------------------------------Admin patient CRUD-----------------------------------------------------


class PatientCreateAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PatientCreateSerializer
    def post(self,request):
        # password = ''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        password = make_password('12345')
        serializer =PatientCreateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            # subject = 'welcome to Clinic'
            # message = f"""Hello {request.data['name']},
            # Your Username is  {request.data['email']},
            # Your Password is {password} """
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [request.data['email'], ]
            # send_mail( subject, message, email_from, recipient_list )
            serializer.save(password = password,role ='patients')
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PatientViewAPI(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role='patients')
    serializer_class =PatientSerializer



class PatientEditAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(role = 'patients')
    serializer_class =PatientSerializer



class PatientDeleteAPI(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = PatientSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')

# ----------------------------Admin Appoinment View ----------------------------------------
class AdminAppoinmentViewAPI(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Appoinment.objects.all()
    serializer_class = BookAppoinmentSerializer 




# -------------------------------------Doctor--------------------------------------------
class DoctorProfile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role = 'doctor')
    serializer_class = DoctorSerializer


class DoctorAvailableAPI(GenericAPIView):
    serializer_class = DoctorAvailableSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
        doc = request.data['doctor']
        week = request.data['week']
        uid = Doctor_availability.objects.filter(doctor__id = doc ,week = week).exists()
        if uid:
            return Response('Data is Already exits',status=status.HTTP_400_BAD_REQUEST)
        serializer = DoctorAvailableSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Data creates Sucessfully',status=status.HTTP_202_ACCEPTED)

class DoctorAvailableUpdateAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor_availability.objects.all()
    serializer_class =DoctorAvailableSerializer


class SlotDeleteAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Doctor_availability.objects.get(pk=pk)
        except Doctor_availability.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = DoctorAvailableSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')

class DoctorAvailableViewAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Doctor_availability.objects.all()
    serializer_class = DoctorAvailableSerializer


class DoctorAppoinmentViewAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookAppoinmentSerializer 
    # def get(self,request):
    #     app = Appoinment.objects.filter(doctor__id = request.user.id)
    #     return Response(app)
    def get_queryset(self,request):
        return Appoinment.objects.filter(doctor__id = request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SetBookStatusAPI(RetrieveUpdateAPIView):
    queryset = Appoinment.objects.all()
    serializer_class = SetBookSerializer



# ------------------------------------------Patients---------------------------------------------

class PatientProfile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role = 'patients')
    serializer_class = PatientSerializer



class BookAppoinmentAPI(CreateAPIView):
    queryset = Appoinment.objects.all()
    serializer_class = BookAppoinmentSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            token = Authenticate(self, request)
            doc = User.objects.get(id = request.data['doctor'])
            patient = request.user
            serializer = BookAppoinmentSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                if doc.role == 'doctor':
                    con = Doctor_availability.objects.filter(doctor__id = request.data['doctor'])
                    b =  datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
                    c = int(b.strftime("%w"))
                    for data in con :
                        if data.week == c:
                            # doc = User.objects.get(id = request.data['doctor'])
                            # print(doc)
                            d = request.data['date']
                            datetime_convert = datetime.strptime(d,"%Y-%m-%d").date()
                            # print(datetime_convert)
                            data = Appoinment.objects.filter(doctor__id = request.data['doctor'],date = datetime_convert)
                            # print(data)
                            x_start = request.data['start_time']
                            # print(x_start)
                            temp_start = datetime.strptime(x_start, '%H:%M:%S').time()
                            for app in data:
                                print(temp_start >= app.start_time)
                                print(temp_start < app.end_time)
                                if  temp_start >= app.start_time and temp_start < app.end_time :
                                    return Response('Doctor Not Available On This Time Please Select Other Time slot')
                            serializer.save(patient = patient)
                            return Response(data={'status': status.HTTP_201_CREATED,
                                                'error': False,
                                                "message":"book Successfully",
                                                "result":serializer.data
                                                },status=status.HTTP_201_CREATED)

                    return Response('Doctor IS not Available ON This Date')
                else:
                    return Response("Please Enter A Valid doctor")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response({'msg':'invalid data'})
        



class BookDeleteAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Appoinment.objects.get(pk=pk)
        except Appoinment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = BookAppoinmentSerializer(user)
        return Response(serializer.data)

    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response('data deleted sucessfully')



class BookAppoinmentViewAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookAppoinmentSerializer 
    # def get(self,request):
    #     app = Appoinment.objects.filter(doctor__id = request.user.id)
    #     return Response(app)
    def get_queryset(self,request):
        return Appoinment.objects.filter(patient__id = request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data is not None:
            return Response(serializer.data)
        else:
            return Response(data={
                                    "Message":'Invalid User.'},
                            status=status.HTTP_400_BAD_REQUEST)













# class BookAppoinmentAPI(CreateAPIView):
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     serializer.save()

    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}

