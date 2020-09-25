from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('tasks/', views.admin_getMonth, name = 'distReport_a_getMonth'),
    url(r'^tasks/(?P<month>[0-9]+)/(?P<distRoleId>[0-9]+)/$', views.admin_getTasks, name='distReport_a_getTasks'),
    path('addTask/', views.admin_addTask, name = 'distReport_a_addtask'),
    path('deleteTask/', views.admin_deleteTask, name = 'distReport_a_deletetask'),
    path('editTask/', views.admin_editTask, name = 'distReport_a_edittask'),
    
    path('ctasks/', views.council_index, name = 'distReport_c_index'),
    path('cgetTasks/', views.council_getTasks, name = 'distReport_c_gettasks'),
    path('csaveTask/', views.council_saveTask, name = 'distReport_c_savetask'),
    path('caddTask/', views.council_addTask, name = 'distReport_c_addtask'),
    
]
