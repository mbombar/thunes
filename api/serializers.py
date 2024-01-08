from rest_framework import serializers
from django.contrib.auth import get_user_model
from Users.models import Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "groups", "email", ""]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
