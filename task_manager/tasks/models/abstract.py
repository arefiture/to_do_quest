import importlib

from django.db import models
from django.utils.text import slugify
from core.models import PrefixedDBModel


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
