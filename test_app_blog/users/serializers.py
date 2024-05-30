from rest_framework import serializers
from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('avatar', )
