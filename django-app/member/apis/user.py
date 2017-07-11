from rest_framework import permissions, generics

from member.serializers import UserSerializer
from member.serializers.user import UserCreationSerializer
from utils.permissions import ObjectIsRequestUser
from ..models import User

__all__ = (
    'UserRetrieveUpdateDestroyView',
    'UserListCreateView',
)


class UserListCreateView(generics.CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    )
