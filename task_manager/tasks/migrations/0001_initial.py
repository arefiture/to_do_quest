# Generated by Django 4.2.17 on 2024-12-20 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'тип сложности',
                'verbose_name_plural': 'Типы сложностей',
                'db_table': 'tasks_difficulty',
                'ordering': ['name'],
                'abstract': False,
                'default_related_name': 'difficulties',
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'тип приоритета',
                'verbose_name_plural': 'Типы приоритетов.',
                'db_table': 'tasks_priority',
                'ordering': ['name'],
                'abstract': False,
                'default_related_name': 'priorities',
            },
        ),
        migrations.CreateModel(
            name='Recurrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'тип повторения',
                'verbose_name_plural': 'Типы повторений',
                'db_table': 'tasks_recurrence',
                'ordering': ['name'],
                'abstract': False,
                'default_related_name': 'recurrence',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'тип статуса',
                'verbose_name_plural': 'Типы статусов',
                'db_table': 'tasks_status',
                'ordering': ['name'],
                'abstract': False,
                'default_related_name': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Краткое описание задачи')),
                ('description', models.CharField(blank=True, max_length=120, null=True, verbose_name='Пояснение к задачи')),
                ('date_start', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задачи')),
                ('date_upd', models.DateTimeField(auto_now=True, verbose_name='Дата обновления задачи')),
                ('date_end', models.DateTimeField(null=True, verbose_name='Дата закрытия задачи')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор задачи')),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.difficulty', verbose_name='Сложность задачи')),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.priority', verbose_name='Приоритет задачи')),
                ('recurrence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.recurrence', verbose_name='Повторение задачи')),
            ],
            options={
                'verbose_name': 'задачу',
                'verbose_name_plural': 'Задачи',
                'db_table': 'tasks_task',
                'ordering': ['id'],
                'abstract': False,
                'default_related_name': 'tasks',
            },
        ),
        migrations.CreateModel(
            name='HistoryTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_upd', models.DateTimeField(auto_now=True, verbose_name='Дата установки статуса')),
                ('comment', models.CharField(blank=True, max_length=60, null=True, verbose_name='Комментарий к статусу')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кто изменил статус')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.status', verbose_name='Текущий статус задачи для пользователя')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'историю задачи',
                'verbose_name_plural': 'Истории задач',
                'db_table': 'tasks_history_task',
                'ordering': ['id'],
                'abstract': False,
                'default_related_name': 'history_tasks',
            },
        ),
        migrations.AddConstraint(
            model_name='historytask',
            constraint=models.UniqueConstraint(fields=('task', 'author'), name='unique_history_task'),
        ),
    ]
