from django.urls import path, include
from django.conf.urls import url
from . import views
from Auth.forms import LoginForm, PasswordChange
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.signup, name='auth_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='Main/m_login.html',authentication_form=LoginForm, extra_context=({'title':'Login','Tab':'login'})), name = 'auth_login'),
    path('passwordChange/', auth_views.PasswordChangeView.as_view(template_name='Auth/passwordChange.html',form_class=PasswordChange, extra_context=({'title':'Change Password','Tab':'profile'})), name = 'auth_passwordChange'),
    path('passwordChangeDone/', auth_views.PasswordChangeDoneView.as_view(template_name='Auth/passwordChangeDone.html',extra_context=({'title':'Password Changed !','Tab':'profile'})), name = 'password_change_done'),
    path('logout/', auth_views.LogoutView.as_view(extra_context=({'title':'Logout','Tab':'logout'})), name = 'auth_logout'),
    path('Club/', views.updateClubProfile, name = 'auth_updateClubProfile'),
    path('Rotaractor/', views.updateUserProfile, name = 'auth_updateUserProfile'),
    url(r'^Rotaractors/view/(?P<username>\w+)/$', views.viewUserProfile, name='auth_viewUserProfile'),
    path('createCouncilAccounts/', views.createCouncilAccounts, name = 'auth_createCouncilAccounts'),
    path('createCouncilPosts/', views.createCouncilPosts, name = 'auth_createCouncilPosts'),
    path('createCouncilMaps/', views.createCouncilMaps, name = 'createCouncilMaps'),
]
