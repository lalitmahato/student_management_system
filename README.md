# Student Management System

This is a student management system built using Django and Docker.

## ERD Diagram
The ERD diagram for the student management system is available at the following URL: [lucid.app](https://lucid.app/lucidchart/fb80dfd6-628b-4305-8fd3-677c2dbc7dda/edit?viewport_loc=-715%2C121%2C2217%2C1095%2C0_0&invitationId=inv_4928a608-8e4c-4b95-b7c0-18a5a67223df)

## Setup Process
### Create ```.env``` file and add the following environment variables:
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

### To run the project:
1. **Build the Docker containers**:
    If you are using ```Makefile``` then run the following command:
    ```bash
    make build
    ```
   **OR** build by using following command:
    ```bash
    docker-compose -f docker-compose.yml up -d --build
    ```
2. **Once the project is successfully build you can use following commands to run the project**:
   - **To run the**:
     If you are using ```Makefile``` then run the following command:
     ```bash
     make up
     ```
     **OR**
     ```bash
     docker-compose -f docker-compose.yml up -d
     ```
   - **To Stop The Project**:
     If you are using ```Makefile``` then run the following command:
     ```bash
     make down
     ```
     **OR**
     ```bash
     docker-compose -f docker-compose.yml down
     ```
   - **To Run Migration**:
     If you are using ```Makefile``` then run the following command:
     ```bash
     make mm
     ```
     ```bash
     make m
     ```
     **OR**
     ```bash
     docker-compose -f docker-compose.yml python manage.py makemigrations
     ```
     ```bash
     docker-compose -f docker-compose.yml python manage.py migrate
     ```
