from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


# Представление для создания нового пользователя (регистрация)
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()  # Получение всех пользователей
    serializer_class = UserSerializer  # Определение сериализатора для User
    permission_classes = [
        AllowAny
    ]  # Доступен всем пользователям (даже не аутентифицированным)


# Сериализатор для кастомного токена с аутентификацией по логину или email
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")  # Получение логина или email
        password = attrs.get("password")  # Получение пароля

        # Поиск пользователя по логину или email
        user = (
            User.objects.filter(username=username_or_email).first()
            or User.objects.filter(email=username_or_email).first()
        )

        if user and user.check_password(password):  # Проверка пароля
            attrs["username"] = user.username  # Установка логина для токена
        else:
            raise serializers.ValidationError("Неверный логин, email или пароль")

        # Возвращаем валидацию родительского класса
        return super().validate(attrs)


# Представление для получения кастомного токена
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = (
        CustomTokenObtainPairSerializer  # Используем кастомный сериализатор
    )
