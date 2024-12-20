from django.contrib.auth import get_user_model
from django.db import models

from tasks.models.abstract import TaskBaseModel
from tasks.models.directories import Status
from tasks.models.task import Task

User = get_user_model()


class HistoryTask(TaskBaseModel):
    """История изменения статусов задач."""
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        verbose_name='Задача'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Кто изменил статус'
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name='Текущий статус задачи для пользователя'
    )
    date_upd = models.DateTimeField(
        verbose_name='Дата установки статуса',
        auto_now=True
    )
    comment = models.CharField(
        verbose_name='Комментарий к статусу',
        max_length=60,
        blank=True,
        null=True
    )

    class Meta(TaskBaseModel.Meta):
        default_related_name = 'history_tasks'
        verbose_name = 'историю задачи'
        verbose_name_plural = 'Истории задач'
        constraints = [
            models.UniqueConstraint(
                fields=('task', 'author'),
                name='unique_history_task'
            )
        ]

    def __str__(self) -> str:
        return f'Задача "{self.task}"; Статус: "{self.status}"'
