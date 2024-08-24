from rest_framework import permissions, viewsets
from users.models import Teacher
from teach import serializers

__all__ = []


class ObjectsViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.TeacherStudentsSerializer
