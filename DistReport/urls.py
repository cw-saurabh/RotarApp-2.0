from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('tasks/', views.admin_getMonth, name = 'distReport_a_getMonth'),
    path('manageAccess/', views.admin_manageAccess, name = 'distReport_a_manageAccess'),
    url(r'^tasks/(?P<monthId>[0-9]+)/(?P<distRoleId>[0-9]+)/$', views.admin_getTasks, name='distReport_a_getTasks'),
    path('addTask/', views.admin_addTask, name = 'distReport_a_addtask'),
    path('deleteTask/', views.admin_deleteTask, name = 'distReport_a_deletetask'),
    path('editTask/', views.admin_editTask, name = 'distReport_a_edittask'),
    path('changePermission/', views.admin_changePermission, name = 'distReport_a_changePermission'),
    url(r'^exportReports/(?P<monthId>[0-9]+)/$', views.admin_exportReports, name='distReport_a_exportReports'),
    url(r'^exportFormatFile/', views.admin_exportFormatFile, name='distReport_a_exportFormatFile'),
    
    path('ctasks/', views.council_index, name = 'distReport_c_index'),
    path('cgetTasks/', views.council_getTasks, name = 'distReport_c_gettasks'),
    path('csaveTask/', views.council_saveTask, name = 'distReport_c_savetask'),
    path('caddTask/', views.council_addTask, name = 'distReport_c_addtask'),
    path('cdeleteTask/', views.council_deleteTask, name = 'distReport_c_deletetask'),
    path('ceditTask/', views.council_editTask, name = 'distReport_c_edittask'),
    
]
