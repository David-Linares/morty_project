from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^export/$', views.pdf, name='pdf'),
    url(r'^export/json', views.download_json, name='json'),
    url(r'^import/', views.import_json, name='import'),
]