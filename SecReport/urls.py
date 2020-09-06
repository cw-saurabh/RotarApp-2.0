from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('report/', views.present_report, name = 'presentReport'),
    path('saveReport/', views.save_report, name = 'saveReport'),
    path('finishReport/', views.finish_report, name = 'finishReport'),
    path('submitReport/', views.submit_report, name = 'submitReport'),
    path('migrateData/',views.migrate_data),
    url(r'^exportReport/(?P<reportId>[\-0-9]+)/$', views.export_report, name='exportReport'),
    url(r'^mailReport/(?P<reportId>[\-0-9]+)/$', views.email_report, name='emailReport'),
]
