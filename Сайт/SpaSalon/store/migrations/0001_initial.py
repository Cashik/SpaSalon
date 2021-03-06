# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-08 22:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, verbose_name='ФИО')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('date_of_birth', models.DateField(null=True, verbose_name='дата рождения')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='аккаунт')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='ФИО')),
                ('post', models.CharField(max_length=50, verbose_name='должность/специальность')),
                ('description', models.CharField(max_length=1000, verbose_name='описание')),
                ('link', models.CharField(max_length=100, verbose_name='ссылка на саоциальную сеть')),
                ('phone', models.CharField(max_length=50, verbose_name='телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('date_of_employment', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата устройства на работу')),
                ('image', models.ImageField(default='images/None/no-img-employees.jpg', upload_to='images/employees', verbose_name='фото')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='аккаунт')),
            ],
            options={
                'verbose_name': 'сотрудник',
                'verbose_name_plural': 'сотрудники',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='заголовок')),
                ('text', models.TextField(verbose_name='полный текст')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата добавления')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateTimeField(verbose_name='Дата посещения')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Заметки, замечания, отзыв')),
                ('user_status', models.BooleanField(default=False, verbose_name='согласен с условиями')),
                ('employee_status', models.BooleanField(default=False, verbose_name='согласен с условиями клиента')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Client', verbose_name='профиль')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Employee', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'посещение',
                'verbose_name_plural': 'посещения',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('time', models.TimeField(verbose_name='продолжительность')),
                ('cost', models.IntegerField(verbose_name='стоимость(руб)')),
                ('description', models.CharField(max_length=1000, verbose_name='описание')),
                ('image', models.ImageField(default='images/None/no-img-employees.jpg', upload_to='images/services', verbose_name='изображение процесса')),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата добавления')),
                ('employees', models.ManyToManyField(to='store.Employee', verbose_name='подходящие сотрудники')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.AddField(
            model_name='record',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.Service', verbose_name='Услуга'),
        ),
    ]
