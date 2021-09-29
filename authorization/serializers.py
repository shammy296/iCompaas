from rest_framework import serializers

from authorization.models import User


class KnoxUserSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return obj.username

    class Meta:
        model = User
        fields = ('id', 'user')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'is_active', 'is_superuser', 'date_joined')
