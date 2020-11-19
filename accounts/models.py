from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.db import models
from locations.models import Region, City, School

import uuid
import os
import random
import string

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('psy_images', filename)


ONLINE = 'online'
OFFLINE = 'offline'

STATUS = (
    (ONLINE, 'Online'),
    (OFFLINE, 'Offline')
)

PSYCHOLOGIST  = 'Психолог'
SPECIALIST    = 'Специалист'
ADMINISTRATOR = 'Администратор'

ACCESS_LEVEL = (
    (PSYCHOLOGIST,  'Психолог'),
    (SPECIALIST,    'Специлиаст'),
    (ADMINISTRATOR, 'Администратор'),
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('User must have email!')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.level = ADMINISTRATOR
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    psy_code = models.PositiveIntegerField(
        verbose_name='Код',
        unique=True,
        blank=True,
        null=True,
    )

    img = models.ImageField(
        verbose_name='Фото', 
        upload_to=get_file_path, 
        null=True,
        blank=True
    )

    first_name = models.CharField(
        max_length=255,
    )

    last_name = models.CharField(
        max_length=255,
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    city = models.ForeignKey(
        City, 
        verbose_name = 'Город', 
        on_delete = models.PROTECT,
        blank=True,
        null=True,
    )

    school = models.ForeignKey(
        School, 
        verbose_name = 'Школа', 
        on_delete = models.PROTECT,
        default=None,
        blank=True,
        null=True,
    )

    level = models.CharField(
        verbose_name = 'Уровень доступа', 
        max_length=50,
        choices = ACCESS_LEVEL,
        default = PSYCHOLOGIST, 
    )

    status = models.CharField(
        verbose_name = 'Статус',
        max_length = 50,
        choices = STATUS,
        default = OFFLINE
    )

    is_spec = models.BooleanField(
        default = False
    )



    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
    )

    objects = UserManager()

    def get_clients_count(self):
        return self.active_students.count()

    def set_psy_code(self):
        try:
            self.psy_code = int(''.join(random.choices(string.digits, k=8)))
            self.save()
        except:
            self.set_psy_code()

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        if not self.psy_code:
            self.set_psy_code()

        if self.level == ADMINISTRATOR:
            self.is_superuser = True
            self.is_staff = True
            self.is_spec = True
        elif self.level == SPECIALIST:
            self.is_spec = True

        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

    class Meta:
        ordering = ('psy_code',)