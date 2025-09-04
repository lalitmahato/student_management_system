from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q, Prefetch, F
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.db import IntegrityError, transaction
from django.contrib import messages
from students.forms import StudentForm, CourseForm, InstructorForm
from students.models import Course, Student, Instructor, Enrollment, Metadata
from user.models import User


# Create your views here.
class IndexPageView(ListView):
    model = Course
    template_name = "index.html"
    context_object_name = "courses"
    paginate_by = 9
    ordering = ['-created_at']


class CourseDetailView(DetailView):
    model = Course
    template_name = "course_detail_view.html"
    context_object_name = "course"

    def get_queryset(self):
        return (
            Course.objects.annotate(enrollment_count=Count("enrollments", distinct=True))
            .prefetch_related(
                Prefetch(
                    "instructors",
                    queryset=Instructor.objects.only("id", "first_name", "middle_name", "last_name"),
                ),
                "metadata",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object

        # Increment view count atomically
        metadata, created = course.metadata.get_or_create(key="views", defaults={"value": "0"})
        with transaction.atomic():
            metadata.value = str(int(metadata.value) + 1)
            metadata.save(update_fields=["value"])

        # Fetch recent courses efficiently
        recent_courses = (
            Course.objects.only("id", "name", "course_code", "thumbnail_image")
            .exclude(id=course.id)
            .order_by("-created_at")[:5]
        )

        context.update({
            "recent_courses": recent_courses,
            "course_instructors": course.instructors.all(),  # already prefetched
            "course_metadata": course.metadata.all(),        # already prefetched
            "total_enrolled_students": course.enrollment_count,
        })
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "course_count": Course.objects.aggregate(courses=Count("id"))["courses"],
            "student_count": Student.objects.aggregate(students=Count("id"))["students"],
            "instructor_count": Instructor.objects.aggregate(instructors=Count("id"))["instructors"],
            "user_count": User.objects.aggregate(users=Count("id", filter=Q(status=True)))["users"],
        })
        return context


class StudentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    login_url = "user:login"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()

    def get_queryset(self):
        search_text = self.request.GET.get('search', None)
        if search_text:
            search_q = (
                    Q(student_id__icontains=search_text) | Q(first_name__icontains=search_text) |
                    Q(last_name__icontains=search_text) | Q(middle_name__icontains=search_text) |
                    Q(phone_number__icontains=search_text) | Q(dob__icontains=search_text) |
                    Q(gender__icontains=search_text) | Q(email__icontains=search_text) |
                    Q(address__icontains=search_text)
            )
        else:
            search_q = Q()
        queryset = Student.objects.filter(search_q).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search', "")
        context.update({
            "search": search_text,
            "filter_fields": {
                'search': search_text
            }
        })
        return context


class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/add_student_form.html"
    success_url = reverse_lazy("students:student_list")
    success_message = "Student added successfully!"
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/edit_student_form.html"
    success_url = reverse_lazy("students:student_list")
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()



class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("students:student_list")
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()


class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    login_url = "user:login"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "instructor"]).exists()

    def get_queryset(self):
        search_text = self.request.GET.get('search', None)
        if search_text:
            search_q = (
                    Q(course_code__icontains=search_text) | Q(name__icontains=search_text) |
                    Q(description__icontains=search_text)
            )
        else:
            search_q = Q()
        if self.request.user.groups.filter(name="instructor").exists():
            user_wise_filter_q = Q(creator=self.request.user)
        else:
            user_wise_filter_q = Q()
        queryset = Course.objects.filter(search_q, user_wise_filter_q).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search', "")
        context.update({
            "search": search_text,
            "filter_fields": {
                'search': search_text
            }
        })
        return context


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/add_course_form.html"
    success_url = reverse_lazy("students:course_list")
    success_message = "Course added successfully!"
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "instructor"]).exists()


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/edit_course_form.html"
    success_url = reverse_lazy("students:course_list")
    login_url = "user:login"

    def test_func(self):
        if self.request.user.groups.filter(name="instructor").exists():
            course_id = self.kwargs.get("pk")
            return Course.objects.filter(id=course_id, creator=self.request.user).exists()
        return self.request.user.groups.filter(name__in=["admin"]).exists()


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("students:course_list")
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "instructor"]).exists()


class InstructorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Instructor
    template_name = "instructor/instructor_list.html"
    context_object_name = "instructors"
    login_url = "user:login"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()

    def get_queryset(self):
        search_text = self.request.GET.get('search', None)
        if search_text:
            search_q = (
                    Q(first_name__icontains=search_text) | Q(middle_name__icontains=search_text) |
                    Q(last_name__icontains=search_text) | Q(email__icontains=search_text) |
                    Q(phone_number__icontains=search_text) | Q(gender__icontains=search_text)
            )
        else:
            search_q = Q()
        queryset = Instructor.objects.filter(search_q).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get('search', "")
        context.update({
            "search": search_text,
            "filter_fields": {
                'search': search_text
            }
        })
        return context


class InstructorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructor/add_instructor_form.html"
    success_url = reverse_lazy("students:instructor_list")
    success_message = "Instructor added successfully!"
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()


class InstructorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructor/edit_instructor_form.html"
    success_url = reverse_lazy("students:instructor_list")
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()


class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model = Instructor
    template_name = "instructor/instructor_delete.html"
    success_url = reverse_lazy("students:instructor_list")
    login_url = "user:login"

    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()


class EnrolledCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Enrollment
    template_name = "enrollment/enrolled_course_list.html"
    context_object_name = "enrollments"
    login_url = "user:login"
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name="student").exists()

    def get_queryset(self):
        search_text = self.request.GET.get("search", "").strip()

        qs = (
            Enrollment.objects.filter(student__user=self.request.user)
            .select_related("course")
            .order_by("-created_at")
        )

        if search_text:
            qs = qs.filter(
                Q(course__course_code__icontains=search_text)
                | Q(course__name__icontains=search_text)
                | Q(course__description__icontains=search_text)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_text = self.request.GET.get("search", "").strip()
        context["search"] = search_text
        context["filter_fields"] = {"search": search_text}
        return context


class EnrollToCourseView(LoginRequiredMixin, View):
    login_url = "user:login"

    def post(self, request, pk):
        student = Student.objects.filter(user=request.user).first()
        course = Course.objects.filter(id=pk).first()
        if not student or not course:
            messages.info(request, "Something Went Wrong!")
            return redirect("students:course_detail", pk=pk)
        try:
            Enrollment.objects.create(student=student, course=course)
            messages.success(request, "Enrolled successfully.")
        except IntegrityError:
            messages.info(request, "You are already enrolled in this course.")

        return redirect("students:course_detail", pk=course.id)
