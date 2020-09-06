from django.urls import path, include
from django.conf.urls import url
from . import views
from Auth.forms import LoginForm, PasswordChange
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='Auth/login.html',authentication_form=LoginForm, extra_context=({'title':'Login','Tab':'login'})), name = 'login'),
    path('passwordChange/', auth_views.PasswordChangeView.as_view(template_name='Auth/passwordChange.html',form_class=PasswordChange, extra_context=({'title':'Change Password','Tab':'profile'})), name = 'passwordChange'),
    path('passwordChangeDone/', auth_views.PasswordChangeDoneView.as_view(template_name='Auth/passwordChangeDone.html',extra_context=({'title':'Password Changed !','Tab':'profile'})), name = 'password_change_done'),
    path('logout/', auth_views.LogoutView.as_view(extra_context=({'title':'Logout','Tab':'logout'})), name = 'logout'),
    path('Club/', views.updateClubProfile, name = 'updateClubProfile'),
    path('Rotaractor/', views.updateUserProfile, name = 'updateUserProfile'),
    url(r'^Rotaractors/view/(?P<username>\w+)/$', views.viewUserProfile, name='viewUserProfile'),
    path('email/', views.email, name = 'email'),
    path('create/', views.createAccounts, name = 'createAccounts')
]
