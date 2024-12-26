from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers import TaskSerializer
from tasks.models import Task


class TaskViewSet(
    CreateModelMixin,
    GenericViewSet
):
    queryset = Task
    serializer_class = TaskSerializer
