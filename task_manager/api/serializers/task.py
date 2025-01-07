from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.serializers.directoriest import (
    DifficultySerializer,
    PrioritySerializer,
    RecurrenceSerializer
)
from api.serializers.user import UserSerializer
from tasks.models import (
    Difficulty,
    HistoryTask,
    Priority,
    Recurrence,
    Status,
    Task
)

User = get_user_model()
CREATED_STATUS = 'created'


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    name = serializers.CharField(
        max_length=60, help_text='Краткое наименование задачи'
    )
    description = serializers.CharField(
        max_length=120, help_text='Пояснение к задачи'
    )
    date_start = serializers.DateTimeField(read_only=True)
    date_add = serializers.DateTimeField(read_only=True)
    date_end = serializers.DateTimeField(read_only=True)
    recurrence = serializers.PrimaryKeyRelatedField(
        queryset=Recurrence.objects.all()
    )
    priority = serializers.PrimaryKeyRelatedField(
        queryset=Priority.objects.all()
    )
    difficulty = serializers.PrimaryKeyRelatedField(
        queryset=Difficulty.objects.all()
    )

    class Meta:
        models = Task
        fields = [
            'id', 'author', 'name', 'description', 'date_start', 'date_add',
            'date_upd', 'date_end', 'recurrence', 'priority'
        ]

    def create(self, validated_data):
        status = get_object_or_404(Status, slug=CREATED_STATUS)
        validated_data['current_status'] = status
        task = super().create(validated_data=validated_data)
        HistoryTask.objects.create(
            task=task,
            author=self.author,
            status=status,
            comment='Задача создана',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author)
        representation['priority'] = RecurrenceSerializer(
            instance.recurrence
        )
        representation['priority'] = PrioritySerializer(instance.recurrence)
        representation['difficulty'] = DifficultySerializer(
            instance.difficulty
        )
        # Возможно, стоит отображать статус
        return representation
