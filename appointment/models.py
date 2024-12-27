from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email adresi gerekli.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    



class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

class Secretary(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='secretary_profile')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='secretaries')

    def __str__(self):
        return self.user.email


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')  
    name = models.CharField(max_length=100)  
    age = models.PositiveIntegerField()  
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])  
    contact = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return self.name


class ExaminationRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='examinations')
    date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Examination for {self.patient.name} by {self.doctor.user.email}"
    

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medicines')

    def __str__(self):
        return self.name


class CalendarBlock(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='calendar_blocks')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()  
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Blocked by {self.doctor.user.email} from {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.patient.name} on {self.date}"
