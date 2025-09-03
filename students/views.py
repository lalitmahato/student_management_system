from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from students.forms import StudentForm
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
