from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'main_home'),
    path('home/', views.home1, name = 'main_home1'),
    path('aboutUs/', views.aboutUs, name = 'main_aboutUs'),
    path('council/', views.council, name = 'main_council'),
    path('whatWeDo/', views.home1, name = 'main_whatWeDo'),
       
]
