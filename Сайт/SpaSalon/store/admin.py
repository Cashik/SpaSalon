from copy import deepcopy
from datetime import timedelta

from django import forms
from django.db.models import Q, Count
from django.forms import model_to_dict, ModelChoiceField
from django.utils import timezone

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

import store

from .models import News, Employee, Service, Record, Client


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    # функция получения полей для формы создания и редактирования
    def get_fields(self, request, obj=None):
        list_display = ['full_name', 'phone', 'account', 'email']
        if not request.user.is_superuser:
            list_display.remove('account')
        return list_display

    # ограничение пользователя на просмотр чужих профилей
    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account=request.user)

    # Функция сохранения, добавляет модель и прикрепляет к создателю, если это не админ
    def save_model(self, request, obj, form, change):
        if not change and not request.user.is_superuser:
            obj.account = request.user
        obj.save()


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    # функция получения полей для формы создания и редактирования
    def get_fields(self, request, obj=None):
        list_display = super(EmployeeAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            list_display.remove('account')
        return list_display

    # ограничение сотрудника на просмотр чужих профилей
    def get_queryset(self, request):
        qs = super(EmployeeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(account=request.user)

    # ограничение сотрудника на редактирование информации
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            readonly_fields = ['full_name', 'post', 'date_of_employment']
            if not request.user.groups.filter(name='Сотрудник').exists():
                readonly_fields.remove('notes')
            return readonly_fields
        else:
            return []


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.client


# форма с методом для валидации записи на посещение
class RecordForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(RecordForm, self).clean()
        employee = cleaned_data.get('employee')
        service = cleaned_data.get('service')
        employee_services = []
        try:
            employee_services = ', '.join([i.name.lower() for i in Service.objects.filter(employees=employee)])
            services = Service.objects.get(Q(employees=employee), Q(id=service.id))
        except Service.DoesNotExist:
            self.add_error('employee',
                           'Сотрудник не предоставляет выбранную услугу. Услуги мастера: {0}.'.format(
                               employee_services))


# регистрация своей модели в админку
@admin.register(Record)
class RecordAdmin(ModelAdmin):
    form = RecordForm

    list_display = ['client_full_name', 'employee_full_name', 'visit_date', 'client_status', 'employee_status']

    def client_full_name(self, obj):
        return obj.client.full_name
    client_full_name.allow_tags = True
    client_full_name.short_description = 'ФИО'

    def employee_full_name(self, obj):
        return obj.employee.full_name
    employee_full_name.allow_tags = True
    employee_full_name.short_description = 'Мастер'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            kwargs["queryset"] = Client.objects.filter(account=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_filter(self, request):
        list_filter = ['visit_date']
        if not request.user.groups.filter(name='Пользователь').exists():
            list_filter.append('client')
        if not request.user.groups.filter(name='Сотрудник').exists():
            list_filter.append('employee')
        return list_filter

    '''
    функция получения полей для формы создания и редактирования,
    собирает все поля для отображения, но вырезает некоторые
    в зависимости от группы текущего пользователя
    '''

    def get_fields(self, request, obj=None):
        self.obj_copy = deepcopy(obj)
        list_display = [f.name for f in Record._meta.get_fields()]
        list_display.remove('id')
        if request.user.groups.filter(name='Пользователь').exists():
            list_display.remove('employee_status')
        if request.user.groups.filter(name='Сотрудник').exists():
            list_display.remove('client_status')
        return list_display

    '''
    Функция установки всех полей в режим "только для чтения",
    если прием уже начался или закончился.
    Доступно только поле "Заметки" всем, кроме сотрудников.
    Так пользователи могут оставить комментарий об посещении.
    '''

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.visit_date < timezone.now():
                readonly_fields = [f.name for f in Record._meta.get_fields()]
                if not request.user.groups.filter(name='Сотрудник').exists():
                    readonly_fields.remove('notes')
                return readonly_fields
        return []

    '''
    функция удаляет кнопку удаления записи для пользователя,
    если прием уже начался или закончился
    '''

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.client_status and obj.employee_status and obj.visit_date < timezone.now() and not request.user.is_superuser and not request.user.groups.filter(
                    name='Сотрудник').exists():
                return False
        return True

    def save_model(self, request, obj, form, change):
        its_employee = request.user.groups.filter(name='Сотрудник').exists()
        its_client = request.user.groups.filter(name='Пользователь').exists()
        if self.obj_copy and (its_client or its_employee) and change:
            obj_dic = model_to_dict(obj)
            obj_old = model_to_dict(self.obj_copy)
            for key, val in obj_dic.items():
                if obj_old[key] != obj_dic[key] and not 'status' in key:
                    if its_client:
                        obj.employee_status = False
                    else:
                        obj.client_status = False
        obj.save()

    # ограничение сотрудника на просмотр чужих профилей
    def get_queryset(self, request):
        qs = super(RecordAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            if request.user.groups.filter(name='Сотрудник').exists():
                return qs.filter(employee__account=request.user)
            else:
                return qs.filter(client__account=request.user)
        return qs

# регистрация своей модели в админку


admin.site.register(News)
admin.site.register(Service)

