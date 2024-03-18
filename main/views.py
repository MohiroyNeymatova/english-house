from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from decimal import Decimal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_courses(request):
    user = request.user
    if user.status in [2, 3]:
        data = CourseSerializer(Course.objects.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_course_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = CourseSerializer(Course.objects.get(id=pk), many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_course(request):
    try:
        user = request.user
        name = request.POST['name']
        price = request.POST['price']
        duration = request.POST['duration']
        if user.status in [2, 3]:
            course = Course.objects.create(name=name, price=price, duration=duration)
            data = {
                'course': CourseSerializer(course).data,
                "message": "Successfully created"
            }
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_course(request, pk):
    user = request.user
    name = request.POST.get('name')
    duration = request.POST.get('duration')
    price = request.POST.get('price')
    if user.status in [2, 3]:
        course = Course.objects.get(id=pk)
        if name is not None:
            course.name = name
        if duration is not None:
            course.duration = duration
        if price is not None:
            course.price = price
        course.save()
        data = {
            'course': CourseSerializer(course).data,
            "message": "Updated"
        }
    else:
        data = {
            "message": 'You are not allowed to use this function'
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_branches(request):
    user = request.user
    if user.status in [2, 3]:
        data = BranchSerializer(Branch.objects.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_branch_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = BranchSerializer(Branch.objects.get(id=pk), many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_branch(request):
    try:
        user = request.user
        name = request.POST['name']
        address = request.POST['address']
        courses = request.POST.getlist('courses')
        if user.status == 2:
            branch = Branch.objects.create(name=name, address=address)
            for i in courses:
                branch.courses.add(Course.objects.get(id=i))
            data = {
                "branch": BranchSerializer(branch, many=False).data,
                'message': "Successfully created"
            }
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_branch(request, pk):
    user = request.user
    name = request.POST.get('name')
    address = request.POST.get('address')
    courses = request.POST.get('courses')
    if user.status in [2, 3]:
        branch = Branch.objects.get(id=pk)
        if name is not None:
            branch.name = name
        if address is not None:
            branch.address = address
        if courses is not None:
            for i in courses:
                branch.courses.add(Course.objects.get(id=i))
        branch.save()
        data = {
            "branch": BranchSerializer(branch, many=False).data,
            "message": "Updated"
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_branch(request, pk):
    user = request.user
    if user.status == 2:
        Branch.objects.get(id=pk).delete()
        data = {
            "message": "Successfully deleted."
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_courses_by_branch_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        branch = Branch.objects.get(id=pk)
        data = CourseSerializer(branch.courses.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def search_for_course_in_branch(request, pk):
    user = request.user
    course = request.POST['course']
    if user.status in [2, 3]:
        branch = Branch.objects.get(id=pk)
        if branch.courses.filter(id=course).count() > 0:
            data = CourseSerializer(branch.courses.get(id=pk), many=False).data
        else:
            data = {
                "message": "There is no this course in this branch"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def remove_course_from_branch(request, pk):
    user = request.user
    course = request.POST['course']
    if user.status in [2, 3]:
        branch = Branch.objects.get(id=pk)
        course2 = Course.objects.get(id=course)
        branch.courses.remove(course2)
        branch.save()
        data = {
            "branch": BranchSerializer(branch, many=False).data,
            "message": "Removed"
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_students(request):
    user = request.user
    if user.status in [2, 3]:
        data = StudentSerializer(Student.objects.all(), many=True).data
    elif user.status == 1:
        groups = Group.objects.filter(teacher__user=user)
        for i in groups:
            students = i.students.all()
        data = PublicStudent(students, many=True).data
    else:
        data = {
            'message': "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_student_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = StudentSerializer(Student.objects.get(id=pk), many=False).data
    elif user.status == 1:
        group = Group.objects.filter(teacher__user=user)
        for i in group:
            stud = i.students.filter(id=pk)
            if stud:
                data = PublicStudent(Student.objects.get(id=pk), many=False).data
                break
            else:
                data = {
                    'message': "It is not your student"
                }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_student(request):
    try:
        request_user = request.user
        branch = request.POST['branch']
        user = request.POST['user']
        passport_number = request.POST['passport_number']
        desiredCourse = request.POST['desiredCourse']
        birth_date = request.POST['birth_date']
        if request_user.status in [2, 3]:
            student = Student.objects.create(branch_id=branch, user_id=user, passport_number=passport_number,
                                             desiredCourse_id=desiredCourse, birth_date=birth_date)
            data = {
                'student': StudentSerializer(student).data,
                "message": "Created"
            }
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_student(request, pk):
    request_user = request.user
    branch = request.POST.get('branch')
    passport_number = request.POST.get('passport_number')
    desiredCourse = request.POST.get('desiredCourse')
    birth_date = request.POST.get('birth_date')
    status = request.POST.get('status')
    debt = request.POST.get('debt')
    student = Student.objects.get(id=pk)
    if request_user.status in [2, 3]:
        if branch is not None:
            student.branch_id = branch
        if passport_number is not None:
            student.passport_number = passport_number
        if desiredCourse is not None:
            student.desiredCourse_id = desiredCourse
        if birth_date is not None:
            student.birth_date = birth_date
        if status is not None:
            student.status = status
        if debt is not None:
            student.debt = debt
        student.save()
        data = StudentSerializer(student, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_student(request, pk):
    user = request.user
    if user.status in [2, 3]:
        Student.objects.get(id=pk).delete()
        data = {
            "message": "Deleted"
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_students_of_branch(request, pk):
    user = request.user
    if user.status in [2, 3]:
        if Student.objects.filter(branch_id=pk).count() > 0:
            data = StudentSerializer(Student.objects.filter(branch_id=pk), many=True).data
        else:
            data = {
                "message": "This branch has no students"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_branch_of_student(request, pk):
    user = request.user
    if user.status in [2, 3]:
        student = Student.objects.get(id=pk)
        branch = student.branch
        data = BranchSerializer(branch, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_student_by_passport_number(request):
    user = request.user
    passport_number = request.GET['passport_number']
    if user.status in [2, 3]:
        if Student.objects.filter(passport_number=passport_number).count() > 0:
            data = StudentSerializer(Student.objects.get(passport_number=passport_number), many=False).data
        else:
            data = {
                "message": "There is no student with this passport number"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_students_by_status(request, pk):
    user = request.user
    if user.status in [2, 3]:
        if Student.objects.filter(status=pk).count() > 0:
            data = StudentSerializer(Student.objects.filter(status=pk), many=True).data
        else:
            data = {
                "message": "There are no students with this status"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_students_by_desired_course(request, pk):
    user = request.user
    if user.status in [2, 3]:
        if Student.objects.filter(desiredCourse_id=pk).count() > 0:
            data = StudentSerializer(Student.objects.filter(desiredCourse_id=pk), many=True).data
        else:
            data = {
                "message": 'There are no students with this desired course'
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def set_debt(request):
    user = request.user
    if user.status in [2, 3]:
        groups = Group.objects.all()
        for i in groups:
            course = i.course
            price = course.price
            for x in i.students.filter(status=2):
                x.debt += price
                x.save()
        data = {
            "success": True
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_unpayed_students(request):
    user = request.user
    if user.status in [2, 3]:
        data = StudentSerializer(Student.objects.filter(debt__gt=0.00), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_payed_students(request):
    user = request.user
    if user.status in [2, 3]:
        if Student.objects.filter(debt=0.00).count() > 0:
            data = StudentSerializer(Student.objects.filter(debt=0.00, status=2), many=True).data
        else:
            data = {
                "message": "There are no payed students"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_payments(request):
    user = request.user
    if user.status in [2, 3]:
        data = PaymentSerializer(Payment.objects.all(), many=True).data
    else:
        data = {
            'message': "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_payment_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = PaymentSerializer(Payment.objects.get(id=pk), many=False).data
    else:
        data = {
            'message': "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_payment(request):
    try:
        user = request.user
        student = request.POST['student']
        money = request.POST['money']
        if user.status in [2, 3]:
            payment = Payment.objects.create(student_id=student, money=money)
            student = Student.objects.get(id=student)
            student.debt -= Decimal(money)
            student.save()
            data = PaymentSerializer(payment, many=False).data
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_payment(request, pk):
    student = request.POST.get('student')
    money = request.POST.get('money')
    user = request.user
    if user.status in [2, 3]:
        payment = Payment.objects.get(id=pk)
        old_student = payment.student
        old_money = payment.money
        if student is not None:
            payment.student = Student.objects.get(id=student)
        if money is not None:
            old_student.debt += Decimal(old_money)
            payment.money = money
            old_student.debt -= Decimal(money)
        old_student.save()
        payment.save()
        data = {
            "success": True
        }
    else:
        data = {
            "success": False
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_payments_of_student(request, pk):
    user = request.user
    if user.status in [2, 3, 4]:
        data = PaymentSerializer(Payment.objects.filter(student_id=pk), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_certificates(request):
    user = request.user
    if user.status in [2, 3]:
        data = CertificateSerializer(Certificate.objects.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_certificate_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = CertificateSerializer(Certificate.objects.get(id=pk), many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_certificate(request):
    try:
        user = request.user
        file = request.FILES['file']
        name = request.POST['name']
        if user.status in [2, 3]:
            certificate = Certificate.objects.create(name=name, file=file)
            data = {
                'certificate': CertificateSerializer(certificate).data,
                "message": "Created"
            }
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_certificate(request, pk):
    user = request.user
    if user.status == 2:
        Certificate.objects.get(id=pk).delete()
        data = {
            "message": "Deleted"
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_certificates_by_name(request):
    user = request.user
    name = request.POST['name']
    if user.status in [2, 3]:
        if Certificate.objects.filter(name=name).count() > 0:
            data = CertificateSerializer(Certificate.objects.filter(name=name), many=True).data
        else:
            data = {
                "message": "There is no certificate under this name"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_teachers(request):
    user = request.user
    if user.status in [2, 3]:
        data = TeacherSerializer(Teacher.objects.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_teacher_by_id(request, pk):
    user = request.user
    if user.status in [2, 3]:
        data = TeacherSerializer(Teacher.objects.get(id=pk), many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_teacher(request):
    try:
        user = request.user
        branch = request.POST['branch']
        passport_number = request.POST['passport_number']
        certificates = request.POST.getlist('certificates')
        birth_date = request.POST['birth_date']
        related_user = request.POST['related_user']
        if user.status in [2, 3]:
            teacher = Teacher.objects.create(branch_id=branch, passport_number=passport_number, birth_date=birth_date,
                                             user_id=related_user)
            for i in certificates:
                teacher.certificates.add(Certificate.objects.get(id=i))
            data = {
                "teacher": TeacherSerializer(teacher, many=False).data,
                'message': "Successfully created"
            }
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_teacher(request, pk):
    user = request.user
    branch = request.POST.get('branch')
    passport_number = request.POST.get('passport_number')
    certificates = request.POST.get('certificates')
    birth_date = request.POST.get('birth_date')
    teacher = Teacher.objects.get(id=pk)
    if user.status in [2, 3]:
        if branch is not None:
            teacher.branch_id = branch
        if passport_number is not None:
            teacher.passport_number = passport_number
        if certificates is not None:
            for i in certificates:
                certificate = Certificate.objects.get(id=i)
                teacher.certificates.add(certificate)
            teacher.save()
        if birth_date is not None:
            teacher.birth_date = birth_date
        teacher.save()
        data = TeacherSerializer(teacher, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_teacher(request, pk):
    user = request.user
    if user.status == 2:
        Teacher.object.get(id=pk).delete()
        data = {
            "message": "Successfully deleted"
        }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_teachers_by_branch(request, pk):
    user = request.user
    if user.status in [2, 3]:
        teachers = Teacher.objects.filter(branch=pk)
        data = TeacherSerializer(teachers, many=True).data
    else:
        data = {
              "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_teacher_by_passport_number(request):
    user = request.user
    passport_number = request.GET['passport_number']
    if user.status in [2, 3]:
        if Teacher.objects.filter(passport_number=passport_number).count() > 0:
            data = TeacherSerializer(Teacher.objects.get(passport_number=passport_number), many=False).data
        else:
            data = {
                "message": "There is no teacher with this passport number"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_groups(request):
    user = request.user
    if user.status in [2, 3]:
        data = GroupSerializer(Group.objects.all(), many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_group_by_id(request, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    if user.status in [2, 3]:
        data = GroupSerializer(group, many=False).data
    elif user.status == 1:
        if group.teacher.user == user:
            data = GroupSerializer(group, many=False).data
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_group(request):
    try:
        user = request.user
        name = request.POST['name']
        teacher = request.POST['teacher']
        course = request.POST['course']
        branch = request.POST['branch']
        students = request.POST.getlist('students')
        if user.status in [2, 3]:
            group = Group.objects.create(name=name, teacher_id=teacher, course_id=course, branch_id=branch)
            for i in students:
                student = Student.objects.get(id=i)
                group.students.add(student)
                student.status = 2
                student.save()
            data = GroupSerializer(group, many=False).data
        else:
            data = {
                "message": "You are not allowed to use this function"
            }
    except Exception as err:
        data = {
            "success": False,
            "error": f'{err}'
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_group(request, pk):
    user = request.user
    name = request.POST.get('name')
    teacher = request.POST.get('teacher')
    course = request.POST.get('course')
    branch = request.POST.get('branch')
    students = request.POST.get('students')
    finished_at = request.POST.get('finished_at')
    group = Group.objects.get(id=pk)
    if user.status in [2, 3]:
        if name is not None:
            group.name = name
        if teacher is not None:
            group.teacher_id = teacher
        if course is not None:
            group.course_id = course
        if branch is not None:
            group.branch_id = branch
        if students is not None:
            for i in students:
                student = Student.objects.get(id=i)
                group.students.add(student)
                student.status = 2
                student.save()
        if finished_at is not None:
            group.finished_at = finished_at
            for i in group.students.all():
                if i.status != 2:
                    break
                else:
                    i.status = 4
                    i.save()
            group.save()
        data = GroupSerializer(group, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_group_by_name(request):
    user = request.user
    group = request.GET['group']
    if user.status in [2, 3]:
        data = GroupSerializer(Group.objects.get(name=group), many=False).data
    elif user.status == 1:
        groups = Group.objects.filter(teacher__user=user)
        if groups.filter(name=group).count() > 0:
            group2 = groups.get(name=group)
            data = GroupSerializer(group2, many=False).data
        else:
            data = {
                "message": "You don't have a group with this name"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_groups_by_teacher(request, pk):
    user = request.user
    if user.status in [2, 3]:
        if Group.objects.filter(teacher_id=pk).exists():
            data = GroupSerializer(Group.objects.filter(teacher_id=pk), many=True).data
        else:
            data = {
                "message": "This teacher has no groups"
            }
    elif user.status == 1:
        if user == Teacher.objects.get(id=pk).user:
            data = GroupSerializer(Group.objects.filter(teacher_id=pk), many=True).data
        else:
            data = {
                "message": "This is not you"
            }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_teacher_by_group(request, pk):
    user = request.user
    if user.status in [2, 3]:
        group = Group.objects.get(id=pk)
        teacher = group.teacher
        data = TeacherSerializer(teacher, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_course_by_group(request, pk):
    user = request.user
    if user.status in [2, 3]:
        group = Group.objects.get(id=pk)
        course = group.course
        data = CourseSerializer(course, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_groups_by_course(request, pk):
    user = request.user
    if user.status in [2, 3]:
        if Course.objects.filter(id=pk).count() > 0:
            course = Course.objects.get(id=pk)
            if Group.objects.filter(course=course):
                data = GroupSerializer(Group.objects.filter(course=course), many=True).data
            else:
                data = {
                    "message": "There is no group with this course"
                }
        else:
            data = {
                "message": "There is no course under this id"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_groups_by_branch(request, pk):
    user = request.user
    branch = Branch.objects.get(id=pk)
    if user.status in [2, 3]:
        if Group.objects.filter(branch=branch):
            data = GroupSerializer(Group.objects.filter(branch=branch), many=True).data
        else:
            data = {
                "message": "There is no group in this branch"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_branch_by_group(request, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    if user.status in [2, 3]:
        branch = group.branch
        data = BranchSerializer(branch, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_students_by_group(request, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    if user.status in [2, 3]:
        students = group.students
        data = StudentSerializer(students, many=True).data
    elif user.status == 1:
        if group.teacher.user == user:
            students = group.students
            data = PublicStudent(students, many=True).data
        else:
            data = {
                "message": "This is not your group!"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_student_to_group(request, pk):
    user = request.user
    student = request.POST['student']
    group = Group.objects.get(id=pk)
    if user.status in [2, 3]:
        group.students.add(student)
        group.save()
        data = GroupSerializer(group, many=False).data
    elif user.status == 1:
        if group.teacher.user == user:
            group.students.add(student)
            group.save()
            data = GroupSerializer(group, many=False).data
        else:
            data = {
                "message": "You are not the teacher of this group"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_group_by_student(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    group = student.group_set.all()
    if user.status in [2, 3]:
        data = GroupSerializer(group, many=True).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def remove_student_from_group(request, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    student = request.POST['student']
    if user.status in [2, 3]:
        group.students.remove(student)
        group.save()
        data = GroupSerializer(group, many=False).data
    elif user.status == 1:
        if group.teacher.user == user:
            group.students.remove(student)
            group.save()
            data = GroupSerializer(group, many=False).data
        else:
            data = {
                "message": "It is not your group"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_note(request, pk):
    student = Student.objects.get(id=pk)
    note = request.POST['note']
    user = request.user
    if user.status in [2, 3]:
        note = Note.objects.create(student=student, note=note, user=user)
        data = NoteSerializer(note, many=False).data
    elif user.status == 1:
        group = Group.objects.get(students=student)
        if group.teacher.user == user:
            note = Note.objects.create(student=student, note=note, user=user)
            data = NoteSerializer(note, many=False).data
        else:
            data = {
                "message": "It is not your student"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_notes(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    if user.status == 4:
        if student.user == user:
            notes = Note.objects.filter(student=student)
            data = NoteSerializer(notes, many=True).data
        else:
            data = {
                "message": "These are not your notes"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def send_notes_to_group(request, pk):
    user = request.user
    group = Group.objects.get(id=pk)
    note = request.POST['note']
    if user.status in [2, 3]:
        students = group.students
        for i in students.all():
            note = Note.objects.create(student=i, user=user, note=note)
            data = NoteSerializer(note, many=False).data
    elif user.status == 1:
        if group.teacher.user == user:
            students = group.students
            for i in students.all():
                note = Note.objects.create(student=i, user=user, note=note)
                data = NoteSerializer(note, many=False).data
        else:
            data = {
                "message": "You are not teacher of this group"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_note(request, pk):
    user = request.user
    if user.status in [2, 3]:
        Note.objects.get(id=pk).delete()
        data = {
            "message": "Deleted"
        }
    elif user.status == 1:
        note = Note.objects.get(id=pk)
        if note.user == user:
            note.delete()
            data = {
                "message": "Deleted"
            }
        else:
            data = {
                "message": "You are not the author of this note"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_mark(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    mark = request.POST['mark']
    group = request.POST['group']
    if user.status == 1:
        groups = Group.objects.get(id=group)
        if groups.teacher.user == user:
            mark = Mark.objects.create(teacher=user, student=student, mark=mark)
            data = MarkSerializer(mark, many=False).data
        else:
            data = {
                "message": "It is not your student"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def see_marks(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    if user.status == 1:
        group = Group.objects.filter(teacher__user=user)
        for i in group.students.all():
            if i == student:
                marks = Mark.objects.filter(student=student)
                data = MarkSerializer(marks, many=True).data
            else:
                data = {
                    "message": "You are not allowed to use this function"
                }
    elif user.status == 4:
        if student.user == user:
            marks = Mark.objects.filter(student=student)
            data = MarkSerializer(marks, many=True).data
        else:
            data = {
                "message": "These are not your marks"
            }
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_plan_lesson(request, pk):
    lesson = PlanLessons.objects.get(id=pk)
    data = PlanLessonSerializer(lesson, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_lesson(request):
    user = request.user
    lesson_number = request.POST['lesson_number']
    theme = request.POST['theme']
    if user.status in [1, 2, 3]:
        plan = PlanLessons.objects.create(lesson_number=lesson_number, theme=theme)
        data = PlanLessonSerializer(plan, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_plan(request, pk):
    user = request.user
    if user.status in [1, 2, 3]:
        plan = Plan.objects.get(id=pk)
        data = PlanSerializer(plan, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_plan(request):
    user = request.user
    course = request.POST['course']
    lessons = request.POST.getlist('lessons')
    if user.status in [1, 2, 3]:
        plan = Plan.objects.create(course_id=course)
        for i in lessons:
            lesson = PlanLessons.objects.get(id=i)
            plan.lessons.add(lesson)
            plan.save()
        data = PlanSerializer(plan, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_plan_by_course(request, pk):
    user = request.user
    if user.status in [1, 2, 3]:
        course = Course.objects.get(id=pk)
        plan = Plan.objects.get(course=course)
        data = PlanSerializer(plan, many=False).data
    else:
        data = {
            "message": "You are not allowed to use this function"
        }
    return Response(data)
