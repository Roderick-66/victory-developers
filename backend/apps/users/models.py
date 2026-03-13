from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role',         'admin')
        extra_fields.setdefault('status',       'active')
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('student',               'Student Intern'),
        ('workplace_supervisor',  'Workplace Supervisor'),
        ('academic_supervisor',   'Academic Supervisor'),
        ('admin',                 'Administrator'),
    ]

    STATUS_CHOICES = [
        ('pending',  'Pending Approval'),
        ('active',   'Active'),
        ('rejected', 'Rejected'),
    ]

    email          = models.EmailField(unique=True)
    full_name      = models.CharField(max_length=255)
    student_number = models.CharField(
                        max_length=20,
                        unique=True,
                        blank=True,
                        null=True,
                        help_text='Required for students only'
                    )
    role           = models.CharField(max_length=30, choices=ROLE_CHOICES)
    status         = models.CharField(
                        max_length=20,
                        choices=STATUS_CHOICES,
                        default='pending'
                    )
    organisation   = models.CharField(
                        max_length=255,
                        blank=True,
                        null=True,
                        help_text='Required for workplace supervisors'
                    )

    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    class Meta:
        verbose_name        = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.full_name} ({self.role}) — {self.status}'
    

class PasswordResetToken(models.Model):
    user       = models.ForeignKey(
                    CustomUser,
                    on_delete=models.CASCADE,
                    related_name='reset_tokens'
                )
    token      = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)

    def is_expired(self):
        # Token expires after 30 minutes
        return timezone.now() > self.created_at + timedelta(minutes=30)

    def __str__(self):
        return f'Reset token for {self.user.email}'