from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    full_name = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    link = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    date_of_employment = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/employees', default='images/None/no-img-employees.jpg')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Service(models.Model):
    name = models.CharField(max_length=50)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    cost = models.IntegerField()
    description = models.CharField(max_length=1000)
    employees = models.ManyToManyField(Employee)
    image = models.ImageField(upload_to='images/services', default='images/None/no-img-employees.jpg')
    add_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Visit(models.Model):
    client_name = models.CharField(max_length=200, verbose_name='ФИО клиента')
    visit_date = models.DateTimeField(default=timezone.now, verbose_name='Дата посещения')
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, verbose_name='Услуга')
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='Работник, принявший клиента')
    notes = models.TextField(null=True, blank=True, verbose_name='Заметки, замечания, отзыв')

    def __str__(self):
        return self.client_name + '  ' + self.visit_date.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
