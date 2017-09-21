from django.conf.urls import url
# from django_pdfkit import PDFView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^export/$', views.pdf_pdfkit, name='pdf'),
    url(r'^export/json', views.download_json, name='json'),
    url(r'^import/', views.import_json, name='import'),
    url(r'^pdf/', views.pdf_pdfkit, name='import'),
    # url(r'^djangopdf/', PDFView.as_view(template_name="pdf/pdf_template.html"), name='import'),
]
