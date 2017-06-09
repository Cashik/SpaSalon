from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    account = models.ForeignKey(User, verbose_name='аккаунт', blank=True, default=1)
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    post = models.CharField(max_length=50, verbose_name='должность/специальность')
    description = models.CharField(max_length=1000, verbose_name='описание')
    link = models.CharField(max_length=100, verbose_name='ссылка на саоциальную сеть')
    phone = models.CharField(max_length=50, verbose_name='телефон')
    email = models.EmailField(verbose_name='E-mail')
    date_of_employment = models.DateTimeField(default=timezone.now, verbose_name='дата устройства на работу')
    image = models.ImageField(upload_to='images/employees', default='images/None/no-img-employees.jpg',
                              verbose_name='фото')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'


class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='продолжительность')
    cost = models.IntegerField(verbose_name='стоимость(руб)')
    description = models.CharField(max_length=1000, verbose_name='описание')
    employees = models.ManyToManyField(Employee, verbose_name='подходящие сотрудники', )
    image = models.ImageField(upload_to='images/services', default='images/None/no-img-employees.jpg',
                              verbose_name='изображение процесса')
    add_date = models.DateTimeField(default=timezone.now, verbose_name='дата добавления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = models.TextField(verbose_name='полный текст')
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name='дата добавления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Client(models.Model):
    account = models.ForeignKey(User, verbose_name='аккаунт')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='ФИО')
    phone = models.CharField(max_length=30, blank=True, verbose_name='телефон')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    date_of_birth = models.DateField(verbose_name='дата рождения', null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Record(models.Model):
    client = models.ForeignKey(Client, verbose_name='профиль',  )
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, verbose_name='Услуга')
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='Мастер')
    visit_date = models.DateTimeField(verbose_name='Дата посещения')
    notes = models.TextField(null=True, blank=True, verbose_name='Заметки, замечания, отзыв')
    client_status = models.BooleanField(default=False, verbose_name='согласие клиента')
    employee_status = models.BooleanField(default=False, verbose_name='согласие мастера')

    def __str__(self):
        return self.client.full_name + ' - ' + self.visit_date.strftime("%d.%m.%Y %H:%M")

    class Meta:
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'
