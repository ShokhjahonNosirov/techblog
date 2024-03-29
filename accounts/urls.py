from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = "register"),
    path('<int:pk>/edit_profile/', UserEditView.as_view(), name = "edit_profile"),
    path('<int:pk>/password/', PasswordsChangeView.as_view(), name = 'password_changing'),
    path('password_success', views.password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), 
        name="password_reset_complete"),
     
]