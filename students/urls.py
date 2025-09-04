"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from students.views import (
    DashboardView, StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView, InstructorListView,
    InstructorCreateView, InstructorUpdateView, InstructorDeleteView, IndexPageView, CourseDetailView
)

app_name = 'students'
urlpatterns = [
    path('', IndexPageView.as_view(), name='index_page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("students/add/", StudentCreateView.as_view(), name="student_add"),
    path("students/<uuid:pk>/edit/", StudentUpdateView.as_view(), name="student_edit"),
    path("students/<uuid:pk>/delete/", StudentDeleteView.as_view(), name="student_delete"),
    path("course/", CourseListView.as_view(), name="course_list"),
    path("course/<uuid:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("course/add/", CourseCreateView.as_view(), name="course_add"),
    path("course/<uuid:pk>/edit/", CourseUpdateView.as_view(), name="course_edit"),
    path("course/<uuid:pk>/delete/", CourseDeleteView.as_view(), name="course_delete"),
    path("instructor/", InstructorListView.as_view(), name="instructor_list"),
    path("instructor/add/", InstructorCreateView.as_view(), name="instructor_add"),
    path("instructor/<uuid:pk>/edit/", InstructorUpdateView.as_view(), name="instructor_edit"),
    path("instructor/<uuid:pk>/delete/", InstructorDeleteView.as_view(), name="instructor_delete"),
]
