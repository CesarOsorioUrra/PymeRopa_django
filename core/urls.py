from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cuenta/login/", auth_views.LoginView.as_view(), name="login"), #voy a importar vista desde lo que ya me ofrece django
    path("cuenta/logout/", auth_views.LogoutView.as_view(), name="logout")
]
