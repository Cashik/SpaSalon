from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
                  url(r'^$', views.about, name='about'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^services/$', views.services, name='services'),
                  url(r'^employees/$', views.employees, name='employees'),
                  url(r'^contacts/$', views.contacts, name='contacts'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
