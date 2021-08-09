from django.contrib import admin
from django.urls import path
from . import views
from .views import UserRegisterView, UserEditView, PasswordsChange
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/',UserRegisterView.as_view(),name='register'),

    path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
    # path('password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/',PasswordsChange.as_view(),name='edit_password'),


]
