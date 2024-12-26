from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from api.serializers.user import UserSerializer

User = get_user_model()


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False, methods=['GET'],
        url_path='me', url_name='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request: Request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
