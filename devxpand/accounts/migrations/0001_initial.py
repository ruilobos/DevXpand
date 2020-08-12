# Generated by Django 3.1 on 2020-08-10 13:59

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'The username can only contain letters, digits or the following characters: @/./+/-/_', 'invalid')], verbose_name='Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Is Active?')),
                ('is_staff', models.BooleanField(blank=True, default=False, verbose_name='Is Staff?')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Joined Date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='Key')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('confirmed', models.BooleanField(blank=True, default=False, verbose_name='Confirmed?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resets', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'New Password',
                'verbose_name_plural': 'New Passwords',
                'ordering': ['-created_at'],
            },
        ),
    ]