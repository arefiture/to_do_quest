import importlib

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from core.models import PrefixedDBModel

User = get_user_model()


class TaskBaseModel(PrefixedDBModel):
    """
    Заготовка для моделей, связанных с задачами.

    С помощью PrefixedDBModel.__init_subclass__ назначает
    новый префикс для таблиц (вместо tasks значение из TASKS).
    """
    @classmethod
    def set_prefix_name(cls):
        """Устанавливает префикс если есть настройка, иначе - дефолт."""
        try:
            # Проверяем наличие константы TASKS в приложении users
            tasks_module = importlib.import_module('users.constants')
            prefix = getattr(tasks_module, 'TASKS', None)
            if prefix:
                cls.prefix_name = prefix
                return None
        except ModuleNotFoundError:
            pass

        # Если TASKS не найдено, используем префикс по умолчанию
        super().set_prefix_name()

    class Meta(PrefixedDBModel.Meta):
        abstract = True


class DirectoryNameSlug(TaskBaseModel):
    """
    Абстрактная модель для справочников с полями name и slug.
    Содержит все их настройки.
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=60,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=60,
        unique=True
    )

    class Meta(TaskBaseModel.Meta):
        abstract = True

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """При отсутствии slug генерируется автоматически от name."""
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Recurrence(DirectoryNameSlug):
    """Модель, характерезующая типы повторений задач."""

    class Meta(DirectoryNameSlug.Meta):
        default_related_name = 'recurrence'
        verbose_name = 'тип повторения'
        verbose_name_plural = 'Типы повторений'


class Priority(DirectoryNameSlug):
    """Модель, характерезующая типы приоритетности задач."""

    class Meta(DirectoryNameSlug.Meta):
        default_related_name = 'priorities'
        verbose_name = 'тип приоритета'
        verbose_name_plural = 'Типы приоритетов.'


class Difficulty(DirectoryNameSlug):
    """Модель, характерезующая типы сложностей задач."""

    class Meta(DirectoryNameSlug.Meta):
        default_related_name = 'difficulties'
        verbose_name = 'тип сложности'
        verbose_name_plural = 'Типы сложностей'


class Status(DirectoryNameSlug):
    """Модель, характерезующая типы статусов задач."""

    class Meta(DirectoryNameSlug.Meta):
        default_related_name = 'statuses'
        verbose_name = 'тип статуса'
        verbose_name_plural = 'Типы статусов'


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
        verbose_name='Дата создания задачи',
        auto_now_add=True
    )
    date_upd = models.DateTimeField(
        verbose_name='Дата обновления задачи',
        auto_now=True
    )
    date_end = models.DateTimeField(
        verbose_name='Дата закрытия задачи',
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

    class Meta(TaskBaseModel.Meta):
        default_related_name = 'tasks'
        verbose_name = 'задачу'
        verbose_name_plural = 'Задачи'

    def __str__(self) -> str:
        return f'Задача: "{self.name}"; Автор: {self.author}'


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
