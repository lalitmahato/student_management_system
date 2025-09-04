import datetime

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from students.models import Course, Instructor


@receiver(post_save, sender=Course)
def course_post_save(sender, instance, created, **kwargs):
    if created:
        today = datetime.date.today()
        month_start_date = today.replace(day=1)

        with transaction.atomic():
            student_count = (
                Course.all_objects.select_for_update()
                .filter(created_at__date__gte=month_start_date)
                .count()
            )
            course_count = str(student_count).zfill(5)
            course_code = f"{today.year}{today.month:02d}{course_count}"
            instance.course_code = course_code
            instance.save()
            instructor = Instructor.objects.filter(user=instance.creator).first()
            if instructor:
                instructor.courses.add(instance)
            else:
                new_instructor = Instructor.objects.create(
                    user=instance.creator,
                    first_name=instance.creator.first_name,
                    middle_name=instance.creator.middle_name,
                    last_name=instance.creator.last_name,
                    phone_number=instance.creator.phone_number,
                    email=instance.creator.email,
                    gender=instance.creator.gender,
                )
                new_instructor.courses.add(instance)
