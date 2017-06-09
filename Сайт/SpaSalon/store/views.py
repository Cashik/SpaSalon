import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import Employee, Service, News


# Create your views here.
def about(request):
    news = News.objects.all().order_by('-created_date', )[:2]
    for n in news:
        n.created_date = n.created_date.strftime(("%d.%m.%Y"))
    pass
    return render(request, 'store/about.html', {'ns': news})


def services(request):
    services = Service.objects.all().order_by('name')
    for service in services:
        service.time = service.time.strftime("%H:%M")
    return render(request, 'store/services.html', {'services': services})


def employees(request):
    employees = Employee.objects.all().order_by('date_of_employment')
    for emp in employees:
        emp.exp = emp.date_of_employment.strftime("%d.%m.%Y")
    return render(request, 'store/employees.html', {'employees': employees})


def contacts(request):
    return render(request, 'store/contacts.html', {})


from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/admin/login/"
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "admin/register.html"
    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        user = form.save()
        user.groups.add(Group.objects.get(name='Пользователь'))
        user.is_staff = True
        user.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
