from django.urls import path
from .views import *
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login',LoginAPI.as_view()),
    path('logout',LogoutView.as_view()),

    # ----------------Admin doctor CRUD ----------------------
    path('doctor-create/',DoctorCreateAPI.as_view()),
    path('doctor-view/',DoctorViewAPI.as_view()),
    path('doctor-edit/<int:pk>',DoctorEditAPI.as_view()),
    path('doctor-delete/<int:pk>',DoctorDeleteAPI.as_view()),


    # --------------------Admin Patient CRUD --------------------------------
    path('patient-create/',PatientCreateAPI.as_view()),
    path('patient-view/',PatientViewAPI.as_view()),
    path('patient-edit/<int:pk>',PatientEditAPI.as_view()),
    path('patient-delete/<int:pk>',PatientDeleteAPI.as_view()),
    path('admin-appoinment/',AdminAppoinmentViewAPI.as_view()),

    # ----------------------------Doctor----------------------------
    path('doctor-profile/<int:pk>',DoctorProfile.as_view()),
    path('slot-add/',DoctorAvailableAPI.as_view()),
    path('slot-update/<int:pk>',DoctorAvailableUpdateAPI.as_view()),
    path('slot-delete/<int:pk>',SlotDeleteAPI.as_view()),
    path('slot-view/',DoctorAvailableViewAPI.as_view()),
    path('doctor-appoinment/',DoctorAppoinmentViewAPI.as_view()),
    path('doctor-appoinment/<int:pk>',SetBookStatusAPI.as_view()),

    # ----------------------------Patient----------------------------
    path('patient-profile/<int:pk>',PatientProfile.as_view()),
    path('book',BookAppoinmentAPI.as_view()),
    path('book-delete/<int:pk>',BookDeleteAPI.as_view()),
    path('patient-appoinment/',BookAppoinmentViewAPI.as_view()),

]
