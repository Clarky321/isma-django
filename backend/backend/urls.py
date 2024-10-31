from django.contrib import admin
from django.urls import path, include
from users.views import CreateUserView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

# Основные пути URL для проекта
urlpatterns = [
    path("admin/", admin.site.urls),  # Панель администратора
    path(
        "users/user/register/", CreateUserView.as_view(), name="register"
    ),  # Регистрация пользователя
    path(
        "users/token/", CustomTokenObtainPairView.as_view(), name="get_token"
    ),  # Получение токена (вход)
    path(
        "users/token/refresh/", TokenRefreshView.as_view(), name="refresh"
    ),  # Обновление токена
    path(
        "users-auth/", include("rest_framework.urls")
    ),  # URL для встроенной аутентификации Django REST
]
