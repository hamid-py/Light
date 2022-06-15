from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, User
# from timedelta.fields import TimedeltaField
from django.utils.timezone import timedelta
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     is_superuser = models.BooleanField(
#         _('superuser status'),
#         default=False, )
#
#     email = models.EmailField(_('email address'), unique=True)
#     is_staff = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.email

class CustomUser(models.Model):
    operator = '0'
    team_lead = '1'
    supervisor = '2'
    head_supervisor = '3'

    position_choice = (
        (operator, 'operator'),
        (team_lead, 'team_lead'),
        (supervisor, 'supervisor'),
        (head_supervisor, 'head_supervisor')
    )
    # username = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.IntegerField(null=True)
    position = models.CharField(choices=position_choice, max_length=50, default=operator)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


class Group(models.Model):
    inbound = 'IN'
    outbound = 'OUT'
    crm = 'CRM'
    group_type = (
        (inbound, 'inbound'),
        (outbound, 'outbound'),
        (crm, 'crm')
    )
    group_type = models.CharField(choices=group_type, max_length=3)
    # total_rest_number = models.IntegerField(blank=True, default=0)
    # total_rest_time = models.IntegerField(blank=True, default=0)
    rest_flag = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    user = models.ManyToManyField(CustomUser, through='Membership', related_name='group_user')

    def __str__(self):
        return self.group_type


class Membership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='membership_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} -- {self.group}'


class Principal(models.Model):
    limit_rest_time = models.DurationField()
    limit_food_time = models.DurationField()
    limit_number_of_rest_number = models.IntegerField(default=1)
    limit_number_of_food_number = models.IntegerField(default=2)
    work_start = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=14)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='principal')
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.group} principal'


class StartRest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='start')
    start_rest = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    in_rest_flag = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user} start rest time'


class EndRest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='end')
    start_rest = models.OneToOneField(StartRest, on_delete=models.CASCADE)
    end_rest = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} end rest time'

    def rest_duration(self):
        return self.end_rest


class AgentHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='history')

    total_rest_time = models.CharField(max_length=50)
    total_rest_seconds = models.PositiveIntegerField(null=True)
    total_error_time = models.CharField(max_length=50)
    total_error_seconds = models.PositiveIntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} rest time'
