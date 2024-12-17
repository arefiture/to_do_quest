import importlib

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

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


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Создание и сохранение пользователя с добавленными логином, почтой, и
        паролем.
        """
        if not username:
            raise ValueError("Логин обязателен.")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Пользователь должен быть is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Пользователь должен быть is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None,
        obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "У вас настроено несколько бэкендов аутентификации и "
                    "поэтому необходимо указать аргумент `backend`."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "бэкенд должен быть строкой пути импорта с точками "
                "(получено %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AuthBaseModel, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "Никнейм",
        max_length=150,
        unique=True,
        help_text=(
            "Обязательно. 150 символов. Только буквы, цифры и @/./+/-/_."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "Такой пользователь уже существует.",
        },
    )
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    email = models.EmailField("Электронная почта", blank=True)
    is_staff = models.BooleanField(
        "Признак доступа к админке",
        default=False,
        help_text="Определяет, может ли пользователь войти в админку.",
    )
    is_active = models.BooleanField(
        "Признак активности профиля",
        default=True,
        help_text=(
            "Указывает, следует ли считать этого пользователя активным. "
            "Отмените выбор вместо удаления."
        ),
    )
    date_joined = models.DateTimeField(
        "Дата регистрации",
        default=timezone.now
    )
    experience = models.PositiveIntegerField(
        verbose_name='Суммарный опыт пользователя',
        default=0
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta(AuthBaseModel.Meta):
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Возвращает полное имя: имя и фамилия через пробел.
        """
        return " ".join(filter(None, [self.first_name, self.last_name]))

    def get_short_name(self):
        """Возвращает короткое имя."""
        return self.first_name or self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Отправляет письмо на почту пользователя."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
