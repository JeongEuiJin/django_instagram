from rest_framework import serializers

from ..models import User

__all__ = (
    'UserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname',
        )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,

    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
        )

    def validate_username(self, username):
        if User.objcets.filter(username=username).exists():
            raise serializers.ValidationError('Username already exist')
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password didn\'t mathch')
        return data

    def save(self, *args,**kwargs):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password1')
        user = User.objcets.create_user(
            username=username,
            password=password,
        )
        return user