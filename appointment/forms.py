from django import forms
from .models import CustomUser,Doctor, Secretary, Patient ,ExaminationRecord, Medicine, CalendarBlock, Appointment


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():            
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {field.label}',
            })


class SecretaryCreationForm(StyledModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="password")

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def save(self, doctor, commit=True):
        user = super().save(commit=False)
        user.is_secretary = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Secretary.objects.create(user=user, doctor=doctor)
        return user

class UserUpdateForm(StyledModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class DoctorProfileUpdateForm(StyledModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization']

class SecretaryProfileUpdateForm(StyledModelForm):
    class Meta:
        model = Secretary
        fields = ['doctor']


class PatientForm(StyledModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'contact']

class ExaminationRecordForm(StyledModelForm):
    class Meta:
        model = ExaminationRecord
        fields = ['patient', 'diagnosis', 'prescription'] 

class MedicineForm(StyledModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description'] 

class CalendarBlockForm(StyledModelForm):
    class Meta:
        model = CalendarBlock
        fields = ['start_time', 'end_time', 'reason'] 

class AppointmentForm(StyledModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'notes'] 



