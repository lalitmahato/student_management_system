from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from students.forms import StudentForm, CourseForm, InstructorForm
from students.models import Course, Student, Instructor
from user.models import User


# Create your views here.
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


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    login_url = "user:login"
    paginate_by = 10

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


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/add_student_form.html"
    success_url = reverse_lazy("students:student_list")
    success_message = "Student added successfully!"
    login_url = "user:login"


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/edit_student_form.html"
    success_url = reverse_lazy("students:student_list")
    login_url = "user:login"


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("students:student_list")
    login_url = "user:login"


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    login_url = "user:login"
    paginate_by = 10

    def get_queryset(self):
        search_text = self.request.GET.get('search', None)
        if search_text:
            search_q = (
                    Q(course_code__icontains=search_text) | Q(name__icontains=search_text) |
                    Q(description__icontains=search_text)
            )
        else:
            search_q = Q()
        queryset = Course.objects.filter(search_q).order_by("-created_at")
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


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/add_course_form.html"
    success_url = reverse_lazy("students:course_list")
    success_message = "Course added successfully!"
    login_url = "user:login"


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/edit_course_form.html"
    success_url = reverse_lazy("students:course_list")
    login_url = "user:login"


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("students:course_list")
    login_url = "user:login"


class InstructorListView(LoginRequiredMixin, ListView):
    model = Instructor
    template_name = "instructor/instructor_list.html"
    context_object_name = "instructors"
    login_url = "user:login"
    paginate_by = 10

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


class InstructorCreateView(LoginRequiredMixin, CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructor/add_instructor_form.html"
    success_url = reverse_lazy("students:instructor_list")
    success_message = "Instructor added successfully!"
    login_url = "user:login"


class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructor/edit_instructor_form.html"
    success_url = reverse_lazy("students:instructor_list")
    login_url = "user:login"


class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model = Instructor
    template_name = "instructor/instructor_delete.html"
    success_url = reverse_lazy("students:instructor_list")
    login_url = "user:login"
