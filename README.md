# Student Management System

Live Demo: https://student-management-system.lalitmahato.com.np/
*User Credential* for admin user:
```
Email: info@lalitmahato.com.np
Password: P@ssw0rd@##!!
```
*Note: Other types of users can register and login using their own email from the system.*

## Overview
The **Student Management System** is a web-based platform built with **Django (MVT architecture)**.  
It provides role-based access for **Admins**, **Instructors**, and **Students**.  
The system uses **PostgreSQL** as the primary database and **Celery + Redis** for handling asynchronous tasks like email notifications.

---

## Users and Roles

### Student
- Register and log in with Django authentication.
- View and enroll in courses.
- Receive confirmation/activation emails notifications (via Celery).
- View grades given by the instructor.

### Instructor
- Create, edit, update, and delete courses.
- Manage course details and content.
- Assign grades/scores to enrolled students.
- Receive notifications of student enrollments.

### Admin
- Full CRUD access to **students, instructors, courses, enrollments, and metadata**.
- Override/update any records.
- Manage advanced configurations.

**Note**: *When the admin creates a new student or instructor, they cannot log in to the system by default.
This is because each student and instructor must be linked to a corresponding User account, and this association
is not automatically established during the creation process. Without this user linkage, authentication is
not possible for the newly added records.*

---

## Features
- **Authentication & Authorization** with Django’s built-in auth system.
- **Student Profile Management** (CRUD operations, unique email validation).
- **Course Management** (unique course codes, instructor-course relations).
- **Enrollment Tracking** with grades/scores and duplicate prevention.
- **Metadata System** (attach key-value annotations to students, courses, instructors, and enrollments).
- **Async Email Notifications** using Celery + Redis.
- **PostgreSQL Database** with strong relational integrity.
- **Frontend UI** built with Django templates, HTML, CSS, and jQuery, bootstrap.
- **Soft Delete** for records.
- **Celery Flower** for monitoring Celery tasks.
- **Docker** for containerization.
- **Makefile** for running commands.
- **Code Quality Check** check using `pylint`.

---

## Tech Stack

| Component        | Technology                                 |
|------------------|--------------------------------------------|
| Backend          | Django (Python)                            |
| Database         | PostgreSQL                                 |
| Message Broker   | Redis                                      |
| Async Tasks      | Celery                                     |
| Auth             | Django Authentication                      |
| Frontend         | Django Templates, HTML, CSS, JS, Bootstrap |
| Containerization | Docker                                     |

---

## System Workflow

1. **User Authentication**  
   - Student, Instructor, Admin login with Django Auth.

2. **Student Actions**  
   - Browse courses → Enroll → View grades.

3. **Instructor Actions**  
   - Create/Edit course → Assign grades.

4. **Admin Actions**  
   - Manage **all entities** with full control.

---

## Advantages
- Clear separation of roles (Admin, Instructor, Student).
- Reliable background processing with **Celery + Redis**.
- Strong relational structure with PostgreSQL.
- Flexible metadata model for advanced use cases (Eg: page view).
- Django’s built-in **security and authentication**.

---

# Setup Process
## Setup Instructions

1. **Clone Repository**
```
https://github.com/lalitmahato/student_management_system.git
```
```
cd student_management_system
```

The setup process for this project is pretty simple because it is dockerized. The only thing required is docker.
The project is using `Makefile` to run the commands, so I recommend to use `Makefile` to run the commands. If your
device don't have `Makefile` installed then you can install it by using following command:
```
pip install makefile
```
The given command will install the `Makefile` on your device. If the `Makefile` does not work then you can enter command 
manually. To setup the project in your device. First create a `.env` file and add the following environment variables:

### Create `.env` file and add the following environment variables:

```dotenv
SECRET_KEY=secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8003
ALLOWED_ORIGINS=http://localhost:8003

# Database Config
DB_ENGINE=django.db.backends.postgresql
DB_NAME=student_management_system
DB_USER=student_management_system
DB_PASSWORD=db_password
DB_HOST=db
DB_PORT=5432

# SMTP Configuration
EMAIL_STATUS=True
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=email
EMAIL_HOST_USER_FROM=email_from
EMAIL_HOST_PASSWORD=password

# Celery Flower Configuration
flower_username=username
flower_password=password

# Pagination Setting
PAGE_SIZE=20

# Redis DB Setup
BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

Change the values of the environment variables according to your setup.

*Note: If you make the `DEBUG=False` the system configuration enforces to secure connection(SSL), this setup might not work on local environment.
So make sure to make `DEBUG=True` if you are working on local environment.*

### Project Setup With `Makefile`
To run the project you need to have docker installed on your device. Also it is better to have `Makefile` installed on your device.

If you are using `Makefile` then you don't need to run multiple commands. To run the project using `Makefile` you can use following commands:
```
make setup
```
The above command will build the docker image, run migrations, seed data to the database from fixture file, collect static files and restart the project.

The above steps are enough to run the project. But if you also want to create super user to login to the system then you can use following command:
```
make csu
```
The above command will create super admin user to login to the system.

### Project Setup Without `Makefile`
If you are not using `Makefile` then you need to run multiple commands.
```
docker-compose -f docker-compose.yml up -d --build
```
The above command will build the docker image. After running the above command you need to run the following commands:
```
docker-compose -f docker-compose.yml python manage.py makemigrations
```
```
docker-compose -f docker-compose.yml python manage.py migrate
```
The given commands will run migrations. After running the above commands you need to seed the data to the database from fixture file. To do that run the following command:
```
docker exec -it student_management_system python manage.py loaddata groups
```
The above command will seed the data to the database from fixture file. After running the above command you need to collect static files. To do that run the following command:
```
docker exec -it student_management_system python manage.py collectstatic --noinput
```
After running the above command you need to restart the project. To do that run the following command:
```
docker-compose -f docker-compose.yml down
```
```
docker-compose -f docker-compose.yml up -d
```
The first command will stop the project and the second command will start the project. This way you can run the project without using `Makefile`.

if you also want to create super user to login to the system then you can use following command:
```
docker exec -it student_management_system python manage.py createsuperuser
```
**Note:** *Initially the user is superuser but it is not `admin` user for the system. To make the user `admin` user
you need to login to the system and go to the admin panel and assign `admin` group to the user.*
