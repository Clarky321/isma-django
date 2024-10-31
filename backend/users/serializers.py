from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Profile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    middle_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "middle_name",
        ]

    def get_middle_name(self, obj):
        # Проверяем наличие профиля у пользователя, чтобы избежать ошибок
        try:
            return obj.profile.middle_name
        except Profile.DoesNotExist:
            return ""

    def create(self, validated_data):
        middle_name = validated_data.pop("middle_name", "")
        user = User.objects.create_user(**validated_data)

        # Создаем профиль, если он отсутствует, и присваиваем middle_name
        profile, created = Profile.objects.get_or_create(user=user)
        profile.middle_name = middle_name
        profile.save()

        return user
