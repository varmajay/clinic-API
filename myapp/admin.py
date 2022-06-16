from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display=['name','email','role','gender','address','id']


admin.site.register(UserToken)

@admin.register(Doctor_availability)
class AdminDoctor_availability(admin.ModelAdmin):
    list_display=['id','doc_id','week','start_time','end_time']
    def doc_id(self, obj):
        return obj.doctor.id

@admin.register(Appoinment)
class AdminAppoinment(admin.ModelAdmin):
    list_display =['id','date','start_time','end_time','date','description','status']
    # def doc_name(self, obj):
    #     return obj.slot.doctor_id.name