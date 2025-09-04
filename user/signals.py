import datetime
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from user.models import User
from students.models import Student, Instructor

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Student":
            today = datetime.date.today()
            month_start_date = today.replace(day=1)

            with transaction.atomic():
                student_count = (
                    Student.all_objects.select_for_update()
                    .filter(created_at__date__gte=month_start_date)
                    .count()
                )
                student_roll_number = str(student_count + 1).zfill(5)
                student_id = f"{today.year}{today.month:02d}{student_roll_number}"

                Student.objects.create(
                    user=instance,
                    student_id=student_id,
                    first_name=instance.first_name,
                    middle_name=instance.middle_name,
                    last_name=instance.last_name,
                    email=instance.email,
                    gender=instance.gender,
                    phone_number=instance.phone_number,
                    dob=instance.date_of_birth,
                )
            Group.objects.get(name="student").user_set.add(instance)
        elif instance.user_type == "Instructor":
            Group.objects.get(name="instructor").user_set.add(instance)
            Instructor.objects.create(
                user=instance,
                first_name=instance.first_name,
                middle_name=instance.middle_name,
                last_name=instance.last_name,
                email=instance.email,
                gender=instance.gender,
                phone_number=instance.phone_number,
            )
