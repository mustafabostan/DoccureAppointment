from django.contrib import admin
from .models import CustomUser, Doctor, Secretary, Patient, Medicine, Appointment, CalendarBlock


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_doctor', 'is_secretary', 'is_staff', 'is_active')
    list_filter = ('is_doctor', 'is_secretary', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__email', 'specialization')
    list_filter = ('specialization',)

@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor')
    search_fields = ('user__email', 'doctor__user__email')
    list_filter = ('doctor',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'contact', 'doctor')
    search_fields = ('name', 'contact', 'doctor__user__email')
    list_filter = ('gender', 'doctor')


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'added_by')
    search_fields = ('name', 'added_by__user__email')
    list_filter = ('added_by',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'notes')
    search_fields = ('patient__name', 'doctor__user__email', 'notes')
    list_filter = ('doctor', 'date')


@admin.register(CalendarBlock)
class CalendarBlockAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'start_time', 'end_time', 'reason')
    search_fields = ('doctor__user__email', 'reason')
    list_filter = ('doctor', 'start_time', 'end_time')
