from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('migrateData/',views.migrate_data),
    path('report/', views.present_report, name = 'secReport_presentReport'),
    path('saveReport/', views.save_report, name = 'secReport_saveReport'),
    url(r'^finishReport/(?P<reportId>.+?)/$', views.finish_report, name='secReport_finishReport'),
    url(r'^submitReport/(?P<reportId>.+?)/$', views.submit_report, name='secReport_submitReport'),
    url(r'^exportReport/(?P<reportId>.+?)/$', views.export_report, name='secReport_exportReport'),
    url(r'^viewReport/(?P<reportId>.+?)/$', views.view_report, name='secReport_viewReport'),
    url(r'^mailReport/(?P<reportId>[\-0-9]+)/$', views.email_report, name='secReport_emailReport'),
]
