"""User Related Models"""

import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from crum import get_current_user


class CreatorModifierInfo(models.Model):
    """Creator and Modifier Info"""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_created',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    modifier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_modified',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField('Created Date Time', null=True, auto_now_add=True)
    modified_at = models.DateTimeField('Modified Date Time', null=True, auto_now=True)
    status = models.BooleanField('delitation_status', default=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            if self.created_at:
                self.modifier = user
            else:
                self.creator = user
        super().save(*args, **kwargs)


class CustomActiveManager(models.Manager):
    """returns only active objects"""
    def get_queryset(self):
        """Returns active objects"""
        return super().get_queryset().filter(status=True)


class CustomAllObjectsManager(models.Manager):
    """returns all objects. both active and not active"""
    def get_queryset(self):
        """Returns all objects"""
        return super().get_queryset().all()


class CustomUserManager(UserManager):
    """Overriding the default User Manager"""
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        username = email
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser, CreatorModifierInfo):
    """Custom User Model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, db_index=True)
    email = models.EmailField(null=True, unique=True)
    gender_select = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    first_name = models.CharField(_("first name"), max_length=150)
    middle_name = models.CharField(_("middle name"), max_length=150, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number = models.CharField(_('phone_number'), null=True, max_length=20)
    photo = models.ImageField(
        _('photo'),
        null=True,
        blank=True,
        upload_to='user/profile/image/%Y/%m/%d/',
        max_length=3000
    )
    date_of_birth = models.DateField(_('date_of_birth'), null=True)
    gender = models.CharField(_('gender'), null=True, choices=gender_select, max_length=200)

    status = models.BooleanField(default=True)
    staff_status = models.BooleanField(default=False)
    customer_status = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        """Returns string representation of user"""
        full_name = self.full_name()
        return full_name if full_name else f"{self.id}"

    def full_name(self):
        """Returns full name"""
        name = ''
        if self.first_name:
            name = self.first_name
        if self.middle_name:
            name = name + ' ' + self.middle_name
        if self.last_name:
            name = name + ' ' + self.last_name
        return name
