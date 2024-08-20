from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Min, Max

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Group
from users.models import Subscription, CustomUser


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available(self, request):
        available_course = set(get_list_or_404(Course, available=True))
        already_subscribe = set(request.user.subscription.courses.all())
        new_course_for_user = available_course - already_subscribe
        if not new_course_for_user:
            return Response(data={"Status": "error", "Detail": "Доступных курсов нет!"},
                            status=status.HTTP_400_BAD_REQUEST)
        data = {"Courses": list(
            {
                "id": course.pk,
                "Title": course.title,
                "Author": course.author,
                "Start date": course.start_date,
                "Price": course.price,
                "Count lesson": course.count_lesson,
            } for course in new_course_for_user
        )}

        return Response(data=data, status=status.HTTP_200_OK)


    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        course = Course.objects.get(pk=pk)
        user = request.user
        if course in user.subscription.courses.all():
            return Response(
                data={"Status": "error", "Detail": "Уже куплен!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.balance.bonuses < course.price:
            return Response(
                data={"Status": "error", "Detail": "Не хватает золота!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.balance.bonuses -= course.price
        user.subscription.courses.add(course)
        if not user.group:
            groups = Group.objects.all()
            groups = [group for group in groups if group.count_users < group.max_users_count] # Отфильтровываем заполненные группы
            if not groups:
                return Response(data={"Status": "error", "Detail": "Свободных групп нет!"},
                status=status.HTTP_400_BAD_REQUEST)
            min_count_user_group = groups[0]
            for group in groups: # Поиск группы с наименьшим кол-во участников.
                if min_count_user_group.count_users > group.count_users:
                    min_count_user_group = group
            user.group = min_count_user_group
        user.save()
        return Response(data={"Status": "success", "Detail": "Курс добавлен!"},
                        status=status.HTTP_201_CREATED)

