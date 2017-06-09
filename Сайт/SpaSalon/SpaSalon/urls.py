from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls, name='admin'),
                  url(r'^admin/register/$', views.RegisterFormView.as_view(), name='register'),
                  url(r'^SpaSalon/', include('store.urls'), name='SpaSalon'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
