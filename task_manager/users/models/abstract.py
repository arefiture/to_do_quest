import importlib

from core.models import PrefixedDBModel


class AuthBaseModel(PrefixedDBModel):
    """
    Заготовка для моделей, связанных с пользователями.

    С помощью PrefixedDBModel.__init_subclass__ назначает
    новый префикс для таблиц (вместо users значение из AUTH).
    """

    @classmethod
    def set_prefix_name(cls):
        """Устанавливает префикс если есть настройка, иначе - дефолт."""
        try:
            # Проверяем наличие константы AUTH в приложении users
            tasks_module = importlib.import_module('users.constants')
            prefix = getattr(tasks_module, 'AUTH', None)
            if prefix:
                cls.prefix_name = prefix
                return None
        except ModuleNotFoundError:
            pass

        # Если AUTH не найдено, используем префикс по умолчанию
        super().set_prefix_name()

    class Meta(PrefixedDBModel.Meta):
        abstract = True
