
# Appointment Management System

**Description**:  
This project is a Django-based appointment management system designed for clinics and healthcare providers. It provides separate functionalities for doctors and secretaries, allowing efficient management of appointments, patients, and schedules.

---

## Features

- **Role-Based Access**:
  - **Doctors**: Manage appointments, patients, examination records, and medicines.
  - **Secretaries**: Handle appointments and calendar schedules.
- **Dynamic Calendar**: Integrated with FullCalendar.js for visualizing appointments and blocks.
- **Appointment Management**: Add, edit, and delete appointments dynamically.
- **Patient Records**: Manage patient information and examination histories.
- **Responsive Design**: User-friendly interface for all devices.
- **Authentication**: Secure login and logout functionalities with role-specific dashboards.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/project-name.git
   cd project-name
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Key Pages

- **Dashboard**: Overview of appointments, patients, and records.
- **Calendar**: View and manage appointments and calendar blocks.
- **Appointments**: Add, edit, or delete appointments.
- **Patients**: Manage patient details and examination records.

---

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript (FullCalendar.js)
- **Database**: SQLite (can be replaced with PostgreSQL or MySQL)

---

## Contact

For questions or support, please contact:  
**Name**: [Mustafa Bostan]  
**Email**: [mustafabostan_38@hotmail.com]  
