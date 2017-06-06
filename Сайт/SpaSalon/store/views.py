import datetime

from django.shortcuts import render
from .models import Employee, Service, News


# Create your views here.
def about(request):
    news = News.objects.all().order_by('-created_date', )[:2]
    for n in news:
        n.created_date = n.created_date.strftime(("%d.%m.%Y"))
    return render(request, 'store/about.html', {"News": news})


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
