from django.contrib import admin
from .models import Course, Group, Lesson


# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'count_lesson']
    list_display_links = ['pk', 'title',]

    def count_lesson(self, obj: Course):
        class Meta:
            verbose_name = "Кол-во уроков"
        return obj.lesson_set.count()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'max_users_count', 'count_users']
    list_display_links = ['pk', 'title',]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass



