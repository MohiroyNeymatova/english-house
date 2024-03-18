from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Branch
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"


class PublicStudent(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['debt']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Payment
        fields = "__all__"


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"


class PlanLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanLessons
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Plan
        fields = "__all__"
