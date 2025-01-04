from django.db import models

from tasks.models.abstract import TaskBaseModel
from tasks.models.directories import Status


class StatusTransitionManager(models.Manager):

    def update_or_create(self, defaults, **kwargs):
        kwargs.pop('current_status')
        defaults['current_status'] = Status.objects.get(
            id=defaults['current_status']
        )
        defaults['next_status'] = Status.objects.get(
            id=defaults['next_status']
        )
        kwargs.setdefault('current_status', defaults['current_status'])
        kwargs.setdefault('next_status', defaults['next_status'])
        return super().update_or_create(defaults, **kwargs)


class StatusTransition(TaskBaseModel):
    current_status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name='Текущий статус',
        related_name='current_statused'
    )
    next_status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name='Следующий статус',
        related_name='next_statused'
    )

    objects = StatusTransitionManager()

    class Meta(TaskBaseModel.Meta):
        verbose_name = 'переход статуса'
        verbose_name_plural = 'Переходы статусов'
