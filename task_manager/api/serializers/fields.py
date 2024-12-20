from rest_framework import serializers


class PasswordField(serializers.CharField):
    """Дефолтные настройки для поля с паролем."""
    def __init__(self, **kwargs):
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        kwargs.setdefault('min_length', 8)
        kwargs.setdefault('style', {'input_type': 'password'})
        super().__init__(**kwargs)
