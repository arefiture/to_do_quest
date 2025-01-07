from django.contrib.auth import get_user_model
from django.db import models

from tasks.models.abstract import TaskBaseModel
from tasks.models.directories import Difficulty, Priority, Recurrence, Status

User = get_user_model()


class Task(TaskBaseModel):
    """Модель, характерезующая задачи."""
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор задачи'
    )
    name = models.CharField(
        verbose_name='Краткое описание задачи',
        max_length=60
    )
    description = models.CharField(
        verbose_name='Пояснение к задачи',
        max_length=120,
        blank=True,
        null=True
    )
    date_start = models.DateTimeField(
        verbose_name='Дата и время, когда нужно начать задачу',
        null=True
    )
    date_add = models.DateTimeField(
        verbose_name='Дата создании задачи',
        auto_now_add=True
    )
    date_upd = models.DateTimeField(
        verbose_name='Дата обновления задачи',
        auto_now=True
    )
    date_end = models.DateTimeField(
        verbose_name='Дата и время, когда задача должна быть выполнена',
        null=True
    )
    recurrence = models.ForeignKey(
        to=Recurrence,
        on_delete=models.CASCADE,
        verbose_name='Повторение задачи'
    )
    priority = models.ForeignKey(
        to=Priority,
        on_delete=models.CASCADE,
        verbose_name='Приоритет задачи'
    )
    difficulty = models.ForeignKey(
        to=Difficulty,
        on_delete=models.CASCADE,
        verbose_name='Сложность задачи'
    )
    current_status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name='Текущий статус',
        default=1
    )

    class Meta(TaskBaseModel.Meta):
        default_related_name = 'tasks'
        verbose_name = 'задачу'
        verbose_name_plural = 'Задачи'

    def __str__(self) -> str:
        return f'Задача: "{self.name}"; Автор: {self.author}'
