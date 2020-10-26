from django.urls import path, include
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # path('migrateData/',views.migrate_data),
    # path('createMonths/',views.createMonths),
    # path('createPermissions/',views.createPermissions),
    # path('addMonth/',views.add_month),
    
    path('report/', views.present_report, name = 'secReport_presentReport'),
    path('secReport/', views.present_report1, name = 'secReport_presentReport1'),
    path('saveReport/', views.save_report, name = 'secReport_saveReport'),
    path('saveSecReport/', views.save_report1, name = 'secReport_saveReport1'),
    url(r'^finishReport/(?P<reportId>.+?)/$', views.finish_report, name='secReport_finishReport'),
    path('finishSecReport/', views.finish_report1, name='secReport_finishReport1'),
    path('submitSecReport/', views.submit_report1, name='secReport_submitReport1'),
    path('editSecReport/', views.edit_report1, name='secReport_editReport1'),
    url(r'^submitReport/(?P<reportId>.+?)/$', views.submit_report, name='secReport_submitReport'),
    url(r'^exportReport/(?P<reportId>.+?)/$', views.export_report, name='secReport_exportReport'),
    url(r'^viewReport/(?P<reportId>.+?)/$', views.view_report, name='secReport_viewReport'),
    url(r'^mailReport/(?P<reportId>.+?)/$', views.email_report, name='secReport_emailReport'),
    path('fetchReports/', views.fetch_reports, name = 'secReport_fetchReports'),

    # Admin panel
    path('secReport/manageAccess/', views.manageAccess, name = 'secReport_manageAccess'),
    path('secReport/responses/', views.responses, name = 'secReport_responses'),
    path('secReport/getPermissions/', views.getPermissions, name = 'secReport_getPermissions'),
    path('secReport/changePermission/', views.changePermission, name = 'secReport_changePermission'),
    

]
