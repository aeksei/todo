from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from task.models import Task
from task_api import serializers, permissions


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    ordering = ["important", "deadline"]  # поля для сортировки

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.order_by_queryset(queryset)

        return queryset

    def order_by_queryset(self, queryset):
        """
        Свой метод сортировки по аналогии с filter_queryset.
        TODO 8. Сортировка заметок по дате, затем по важности
        """
        return queryset.order_by(*self.ordering)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # добавили автора для сохранения


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    TODO 1. Создавать, изменять и удалять заметки
    """
    permission_classes = [IsAuthenticated & permissions.OnlyAuthorEdit]
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer


class PublicTaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(public=True).exclude(author=self.request.user)

        return queryset
