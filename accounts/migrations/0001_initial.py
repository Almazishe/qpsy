# Generated by Django 3.1.3 on 2020-11-12 18:59

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('psy_code', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Код')),
                ('img', models.ImageField(blank=True, null=True, upload_to=accounts.models.get_file_path, verbose_name='Фото')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('level', models.CharField(choices=[('Психолог', 'Психолог'), ('Специалист', 'Специлиаст'), ('Администратор', 'Администратор')], default='Психолог', max_length=50, verbose_name='Уровень доступа')),
                ('status', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='offline', max_length=50, verbose_name='Статус')),
                ('is_spec', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='locations.city', verbose_name='Город')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('school', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='locations.school', verbose_name='Школа')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('psy_code',),
            },
        ),
    ]
