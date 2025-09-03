from django.contrib import admin
from students.models import Metadata, Student, Course, Instructor, Enrollment

# Register your models here.
@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'created_at', 'modified_at')
    search_fields = ('id', 'key', 'value')
    list_filter = ('created_at', 'modified_at')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'email', 'dob', 'created_at', 'modified_at')
    search_fields = ('id', 'first_name', 'middle_name', 'last_name', 'email')
    list_filter = ('dob',)
    filter_horizontal = ('metadata',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course_code', 'created_at', 'modified_at')
    search_fields = ('name', 'course_code', 'description')
    filter_horizontal = ('metadata',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'created_at', 'modified_at')
    search_fields = ('first_name', 'last_name', 'email')
    filter_horizontal = ('courses', 'metadata')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'enrollment_datetime', 'created_at', 'modified_at')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    list_filter = ('enrollment_datetime',)
    filter_horizontal = ('metadata',)
