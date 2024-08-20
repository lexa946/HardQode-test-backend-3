from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from courses.models import Course, Group

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    group = models.ForeignKey(
        to=Group,
        on_delete=models.DO_NOTHING,
        verbose_name="Группа",
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            balance = Balance.objects.create()
            balance.user = self
            subscription = Subscription.objects.create()
            subscription.user = self
            super(CustomUser, self).save(*args, **kwargs)
            balance.save()
            subscription.save()
        else:
            super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)


    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    bonuses = models.IntegerField(
        validators=[MinValueValidator(0),],
        verbose_name="Бонусы",
        default=1000,
    )

    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
    )

    def __str__(self):
        return f"Баланс пользователя {self.user}"

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)





class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
    )
    courses = models.ManyToManyField(
        to=Course,
        # on_delete=models.CASCADE,
        verbose_name="Курс",
        blank=True,
    )

    @property
    def count_courses(self):
        return self.courses.count()


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

