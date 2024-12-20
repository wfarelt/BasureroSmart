# Generated by Django 5.1.2 on 2024-11-28 23:39

import core.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='WasteContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del Contenedor')),
                ('location', models.CharField(max_length=255, verbose_name='Ubicación del Contenedor')),
                ('status', models.CharField(choices=[('Operativo', 'Operativo'), ('Lleno', 'Lleno'), ('Mantenimiento', 'Mantenimiento')], default='Operativo', max_length=20)),
                ('last_maintenance', models.DateTimeField(auto_now_add=True, verbose_name='Último Mantenimiento')),
                ('capacity', models.PositiveIntegerField(default=100, verbose_name='Capacidad del Contenedor')),
                ('current_level', models.PositiveIntegerField(default=0, verbose_name='Nivel Actual de Residuos')),
            ],
        ),
        migrations.CreateModel(
            name='WasteType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Tipo de Residuo')),
                ('bonus_points', models.PositiveIntegerField(verbose_name='Bonificación en Puntos')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('total_points', models.PositiveIntegerField(default=0, verbose_name='Total de Puntos')),
                ('image_perfil', models.ImageField(blank=True, null=True, upload_to=core.models.user_directory_path, verbose_name='Imagen de Perfil')),
                ('image_perfil2', models.ImageField(blank=True, null=True, upload_to=core.models.user_directory_path, verbose_name='Imagen de Perfil 2')),
                ('image_perfil3', models.ImageField(blank=True, null=True, upload_to=core.models.user_directory_path, verbose_name='Imagen de Perfil 3')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Transacción')),
                ('points_awarded', models.PositiveIntegerField(verbose_name='Puntos Otorgados')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wastecontainer', verbose_name='Contenedor')),
                ('waste_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wastetype', verbose_name='Tipo de Residuo')),
            ],
            options={
                'verbose_name': 'Transacción',
                'verbose_name_plural': 'Transacciones',
            },
        ),
    ]
