"""
FAQ:
В: Зачем пакет, когда только две модели + менеджер?
О: Есть будет расширение. К примеру, добавятся подписчики. Ну и
единый вид должен быть.
"""
from users.models.user import User, UserManager

__all__ = [
    'User',
    'UserManager'
]
