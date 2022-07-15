from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.only(
        'name',
        'surname',
        'email'
    ).all()
    serializer_class = UserSerializer
    search_fields = ('name', 'surname', 'email', )
