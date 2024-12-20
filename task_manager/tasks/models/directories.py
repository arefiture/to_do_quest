from tasks.models.abstract import DirectoryNameSlug


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
