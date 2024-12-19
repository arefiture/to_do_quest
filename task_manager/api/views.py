from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Пользователь успешно зарегистрирован'},
            status=status.HTTP_201_CREATED
        )
