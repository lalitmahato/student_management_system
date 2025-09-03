from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from students.models import Course, Student, Instructor
from user.models import User


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'user:login'
    template_name = "students/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "course_count": Course.objects.aggregate(courses=Count("id"))["courses"],
            "student_count": Student.objects.aggregate(students=Count("id"))["students"],
            "instructor_count": Instructor.objects.aggregate(instructors=Count("id"))["instructors"],
            "user_count": User.objects.aggregate(users=Count("id", filter=Q(status=True)))["users"],
        })
        return context
