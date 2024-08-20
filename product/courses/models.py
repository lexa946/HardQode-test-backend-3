from django.db import models
from django.conf import settings


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    price = models.FloatField(
        max_length=250,
        verbose_name="Стоимость",
        default=0.0,
    )

    available = models.BooleanField(
        default=False,
        verbose_name="Доступность"
    )

    @property
    def count_subscribers(self):
        return self.subscription_set.count()

    @property
    def count_lesson(self):
        return self.lesson_set.count()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=250,
        verbose_name="Название",
        default="Новая группа"
    )
    max_users_count = models.IntegerField(
        verbose_name="Максимальное кол-во пользователей",
        default=30,
    )

    @property
    def filled_percent(self):
        return self.count_users / self.max_users_count * 100

    @property
    def count_users(self):
        return self.customuser_set.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
