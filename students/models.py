import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from user.models import CreatorModifierInfo, User

# Create your models here.
gender_select = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))

class Metadata(CreatorModifierInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    key = models.CharField(max_length=500, db_index=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"


class Student(CreatorModifierInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    student_id = models.CharField(max_length=500, db_index=True, unique=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=500, null=True)
    gender = models.CharField(max_length=200, choices=gender_select, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    metadata = models.ManyToManyField(
        Metadata, related_name="students", blank=True
    )

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name()} ({self.student_id})"


class Course(CreatorModifierInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    course_code = models.CharField(max_length=20, unique=True, null=True)
    thumbnail_image = models.ImageField(upload_to='course_thumbnails/%Y/%m/%d', null=True, max_length=2000)
    name = models.CharField(max_length=100, null=True)
    short_description = models.TextField(null=True)
    description = RichTextField(config_name='limited', null=True)
    metadata = models.ManyToManyField(
        Metadata, related_name="courses", blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.course_code})"


class Instructor(CreatorModifierInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    gender = models.CharField(max_length=200, choices=gender_select, null=True)
    courses = models.ManyToManyField(Course, related_name="instructors", blank=True)
    metadata = models.ManyToManyField(
        Metadata, related_name="instructors", blank=True
    )

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


class Enrollment(CreatorModifierInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, related_name="enrollments", null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name="enrollments", null=True
    )
    enrollment_datetime = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True,
        null=True,
    )
    metadata = models.ManyToManyField(
        Metadata, related_name="enrollments", blank=True
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} | {self.course}"
