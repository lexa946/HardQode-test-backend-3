# Generated by Django 4.2.10 on 2024-08-19 21:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_available_course_price_group_max_users_count_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='bonuses',
            field=models.IntegerField(default=1000, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Бонусы'),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='courses.group', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='courses',
            field=models.ManyToManyField(null=True, to='courses.course', verbose_name='Курс'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
