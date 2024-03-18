from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(AbstractUser):
    status = models.IntegerField(choices=(
        (1, 'teacher'),
        (2, 'admin'),
        (3, 'reception'),
        (4, 'student')
    ), blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=25, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Student(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    passport_number = models.CharField(max_length=250)
    status = models.IntegerField(choices=(
        (1, 'waiting'),
        (2, 'in_group'),
        (3, 'left'),
        (4, 'graduated')
    ), default=1)
    desiredCourse = models.ForeignKey(Course, on_delete=models.PROTECT)
    debt = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=25, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Certificate(models.Model):
    file = models.FileField(upload_to='certificates/')
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    passport_number = models.CharField(max_length=250)
    certificates = models.ManyToManyField(Certificate)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.first_name


class Group(models.Model):
    name = models.CharField(max_length=250)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student)
    started_at = models.DateField(auto_now_add=True)
    finished_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Mark(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mark = models.FloatField()
    date = models.DateField(auto_now_add=True)


class PlanLessons(models.Model):
    lesson_number = models.IntegerField()
    theme = models.CharField(max_length=250)

    def __str__(self):
        return self.theme


class Plan(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lessons = models.ManyToManyField(PlanLessons)