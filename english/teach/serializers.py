from rest_framework import serializers
from users.models import Teacher


class TeacherStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'students']
