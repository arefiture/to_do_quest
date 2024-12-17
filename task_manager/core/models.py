from django.db import models

from core.utils import to_snake_case


class PrefixedDBModel(models.Model):
    """Заготовка для установки префикса пред названием таблиц."""

    class Meta:
        abstract = True

    @classmethod
    def set_prefix_name(cls):
        """Устанавливает префикс по умолчанию - имя приложения."""
        cls.prefix_name = cls._meta.app_label

    @classmethod
    def set_ordering(cls):
        """
        Устанавливает правильное значение для ordering в зависимости от
        наличия поля name.

        Поведение:
        - Если name имеется - вернёт ['name']
        - Если name отсутствует - вернёт ['id']
        """
        if hasattr(cls, 'name'):
            cls.Meta.ordering = ['name']
        else:
            cls.Meta.ordering = ['id']

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        table_name = to_snake_case(cls.__name__)
        cls.set_prefix_name()
        cls.Meta.db_table = f'{cls.prefix_name}_{table_name}'
        cls.set_ordering()
