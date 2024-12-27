from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SecretaryCreationForm, PatientForm, ExaminationRecordForm, MedicineForm, CalendarBlockForm, AppointmentForm, UserUpdateForm, DoctorProfileUpdateForm, SecretaryProfileUpdateForm
from .models import CustomUser, Doctor, Secretary, ExaminationRecord, Patient, Medicine, CalendarBlock, Appointment

def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Geçersiz e-posta veya şifre.")
    return render(request, 'appointment/login.html')


def custom_logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('dashboard')


@login_required
def profile_view(request):
    user = request.user
    if user.is_doctor:
        profile = user.doctor_profile
    elif user.is_secretary:
        profile = user.secretary_profile
    else:
        profile = None

    return render(request, 'appointment/profile.html', {'user': user, 'profile': profile})



@login_required
def edit_profile_view(request):
    user = request.user
    if user.is_doctor:
        profile = user.doctor_profile
        profile_form_class = DoctorProfileUpdateForm
    elif user.is_secretary:
        profile = user.secretary_profile
        profile_form_class = SecretaryProfileUpdateForm
    else:
        profile = None
        profile_form_class = None

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if profile_form_class:
            profile_form = profile_form_class(request.POST, instance=profile)
        else:
            profile_form = None

        if user_form.is_valid() and (not profile_form or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = profile_form_class(instance=profile) if profile_form_class else None

    return render(request, 'appointment/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })



@login_required
def index(request):
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'recent_doctors': Doctor.objects.all()[:5],
        'recent_patients': Patient.objects.all()[:5],
    }
    return render(request, 'appointment/index.html', context)


@login_required
def add_secretary(request):
    print(f"Giriş yapan kullanıcı: {request.user}, is_doctor: {request.user.is_doctor}")    
    
    if not request.user.is_doctor:
        messages.error(request, "Bu işlem yalnızca doktorlar tarafından yapılabilir.")
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
    except AttributeError:
        messages.error(request, "Hesabınızla ilişkilendirilmiş bir doktor profili bulunamadı.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = SecretaryCreationForm(request.POST)
        if form.is_valid():
            form.save(doctor=doctor)
            messages.success(request, "Sekreter başarıyla eklendi.")
            return redirect('dashboard')
    else:
        form = SecretaryCreationForm()

    return render(request, 'appointment/add_secretary.html', {'form': form})


@login_required
def secretary_list(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    secretaries = Secretary.objects.filter(doctor=doctor)
    return render(request, 'appointment/secretary_list.html', {'secretaries': secretaries})


@login_required
def edit_secretary(request, secretary_id):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    secretary = Secretary.objects.get(id=secretary_id, doctor=doctor)
    if request.method == 'POST':
        form = SecretaryCreationForm(request.POST, instance=secretary.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('secretary_list')
    else:
        form = SecretaryCreationForm(instance=secretary.user)
    return render(request, 'appointment/edit_secretary.html', {'form': form, 'secretary': secretary})


@login_required
def delete_secretary(request, secretary_id):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    secretary = Secretary.objects.get(id=secretary_id, doctor=doctor)
    if request.method == 'POST':
        user = secretary.user
        secretary.delete()
        user.delete()
        return redirect('secretary_list')
    return render(request, 'appointment/delete_secretary.html', {'secretary': secretary})



@login_required
def patient_list(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    patients = doctor.patients.all()
    return render(request, 'appointment/patient_list.html', {'patients': patients})

@login_required
def add_patient(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = doctor
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'appointment/add_patient.html', {'form': form})


@login_required
def edit_patient(request, patient_id):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    patient = Patient.objects.get(id=patient_id, doctor=doctor)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'appointment/edit_patient.html', {'form': form, 'patient': patient})


@login_required
def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        patient.delete()
        return redirect('patient_list')
    return HttpResponseForbidden("This action is not allowed.")



@login_required
def examination_list(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    examinations = ExaminationRecord.objects.filter(doctor=doctor)
    return render(request, 'appointment/examination_list.html', {'examinations': examinations})


@login_required
def add_examination(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        form = ExaminationRecordForm(request.POST)
        if form.is_valid():
            examination = form.save(commit=False)
            examination.doctor = doctor
            examination.save()
            return redirect('examination_list')
    else:
        form = ExaminationRecordForm()
    return render(request, 'appointment/add_examination.html', {'form': form})


def edit_examination(request, examination_id):
    examination = get_object_or_404(ExaminationRecord, id=examination_id)
    if request.method == 'POST':
        form = ExaminationRecordForm(request.POST, instance=examination)
        if form.is_valid():
            form.save()
            return redirect('examination_list')  
    else:
        form = ExaminationRecordForm(instance=examination)
    return render(request, 'appointment/edit_examination.html', {'form': form})


def delete_examination(request, examination_id):
    if request.method == 'POST':
        examination = get_object_or_404(ExaminationRecord, id=examination_id)
        examination.delete()
        return redirect('examination_list')
    return HttpResponseForbidden("This action is not allowed.")

@login_required
def medicine_list(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    medicines = Medicine.objects.filter(added_by=doctor)
    return render(request, 'appointment/medicine_list.html', {'medicines': medicines})

@login_required
def add_medicine(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.added_by = doctor
            medicine.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'appointment/add_medicine.html', {'form': form})


@login_required
def edit_medicine(request, medicine_id):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    medicine = Medicine.objects.get(id=medicine_id, added_by=doctor)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'appointment/edit_medicine.html', {'form': form, 'medicine': medicine})

@login_required
def delete_medicine(request, medicine_id):
    if request.method == 'POST':        
        medicine = get_object_or_404(Medicine, id=medicine_id)        
        medicine.delete()        
        return redirect('medicine_list')    
    return HttpResponseForbidden("This action is not allowed.")


@login_required
def calendar_view(request):
    if not request.user.is_doctor and not request.user.is_secretary:
        return redirect('dashboard')
    doctor = request.user.doctor_profile if request.user.is_doctor else request.user.secretary_profile.doctor
    blocks = CalendarBlock.objects.filter(doctor=doctor)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'appointment/calendar.html', {'blocks': blocks, 'appointments': appointments})


@login_required
def add_calendar_block(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        form = CalendarBlockForm(request.POST)
        if form.is_valid():
            block = form.save(commit=False)
            block.doctor = doctor
            block.save()
            return redirect('calendar')
    else:
        form = CalendarBlockForm()
    return render(request, 'appointment/add_calendar_block.html', {'form': form})

@login_required
def add_appointment(request):
    if not request.user.is_doctor and not request.user.is_secretary:
        return redirect('dashboard')
    doctor = request.user.doctor_profile if request.user.is_doctor else request.user.secretary_profile.doctor
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            overlapping_blocks = CalendarBlock.objects.filter(
                doctor=doctor,
                start_time__lte=appointment.date,
                end_time__gte=appointment.date
            )
            if overlapping_blocks.exists():
                form.add_error('date', 'Bu tarih ve saatte takvim engellemesi var.')
            else:
                appointment.save()
                return redirect('calendar')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/add_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    if request.user.is_doctor:
        doctor = request.user.doctor_profile
        appointments = Appointment.objects.filter(doctor=doctor)
    elif request.user.is_secretary:
        doctor = request.user.secretary_profile.doctor
        appointments = Appointment.objects.filter(doctor=doctor)
    else:
        return redirect('dashboard')

    return render(request, 'appointment/appointment_list.html', {'appointments': appointments})


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment/edit_appointment.html', {'form': form})


def delete_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return redirect('appointment_list')
    return HttpResponseForbidden("This action is not allowed.")


def calendar_events(request):
    events = []
    for appointment in Appointment.objects.all():
        events.append({
            'title': f'Appointment: {appointment.patient.name}',
            'start': appointment.date.isoformat(),
            'end': appointment.date.isoformat(),
        })
    for block in CalendarBlock.objects.all():
        events.append({
            'title': block.reason,
            'start': block.start_time.isoformat(),
            'end': block.end_time.isoformat(),
            'color': 'red'
        })
    return JsonResponse(events, safe=False)