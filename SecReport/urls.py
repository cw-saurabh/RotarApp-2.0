from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('migrateData/',views.migrate_data),
    
    path('report/', views.present_report, name = 'presentReport'),
    path('saveReport/', views.save_report, name = 'saveReport'),
    url(r'^finishReport/(?P<reportId>.+?)/$', views.finish_report, name='finishReport'),
    url(r'^submitReport/(?P<reportId>.+?)/$', views.submit_report, name='submitReport'),
    url(r'^exportReport/(?P<reportId>[\-0-9]+)/$', views.export_report, name='exportReport'),
    url(r'^mailReport/(?P<reportId>[\-0-9]+)/$', views.email_report, name='emailReport'),
]
