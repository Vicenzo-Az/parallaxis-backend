"""
Rotas do bounded context `users`, incluídas em config/urls.py sob /api/users/.

A implementar conforme as views forem criadas em views.py.
"""
from django.urls import path

from apps.users.api.views import ChangePasswordView, ProfileView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("me/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
