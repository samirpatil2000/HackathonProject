from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='home'),

    path('register/', views.registration_view, name='register'),

    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html')
         , name='password_reset_confirm'),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),
         name='password_change'),

 ]