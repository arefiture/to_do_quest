from rest_framework import serializers

from tasks.models.abstract import DirectoryNameSlug
from tasks.models.directories import Difficulty, Priority, Recurrence


class DirectorySerializer(serializers.ModelSerializer):
    """Заготовка под сериалайзеры справочников."""
    name = serializers.CharField(
        max_length=60,
        help_text='Наименование сложности'
    )
    slug = serializers.SlugField(
        max_length=60
    )

    class Meta:
        abstract = True  # Указываю для понимания
        model = DirectoryNameSlug
        fields = ['id', 'name', 'slug']


class DifficultySerializer(DirectorySerializer):
    """Сериалайзер справочника сложности."""

    class Meta:
        model = Difficulty
        fields = DirectorySerializer.Meta.fields


class PrioritySerializer(DirectorySerializer):
    """Сериалайзер справочника приоритетов."""

    class Meta:
        model = Priority
        fields = DirectorySerializer.Meta.fields


class RecurrenceSerializer(DirectorySerializer):
    """Сериалайзер справочника типов повторений."""

    class Meta:
        model = Recurrence
        fields = DirectorySerializer.Meta.fields
