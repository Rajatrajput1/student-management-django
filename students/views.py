from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Student
from .forms import StudentForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedReadOnly

from .serializers import StudentSerializer

# Create your views here.

@login_required
def student_list(request):
    students = Student.objects.all().order_by("student_id")

    search = request.GET.get('search')
    if search:
        students = students.filter(
            name__icontains = search
        )


    course = request.GET.get("course")
    if course:
        students = students.filter(course=course)

    courses = Student.objects.values_list(
                "course",
                flat=True
            ).distinct()

    paginator = Paginator(students,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)
    
    return render(
        request,
        "students/student_list.html",
        {
            "students" : page_obj,
            "query_params": query_params,
            "courses" : courses,
            "search": search,
            "course": course
        }

    )



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("student_list")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "students/login.html",
        {"form": form}
    )

@require_POST
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()


    return render(
        request, 
        "students/student_create.html",
        {"form": form}
        )


@login_required
def student_update(request,student_id):
    student = student = get_object_or_404(
                        Student,
                        student_id=student_id
                    )

    if request.method == "POST":
            form = StudentForm(request.POST, instance=student)
    
            if form.is_valid():
                form.save()
                return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    
    
    return render(
        request, 
        "students/student_create.html",
        {"form": form, "student" : student}
        )


@login_required
@require_POST
def student_delete(request, student_id):
    student = get_object_or_404(
        Student,
        student_id=student_id
    )

    student.delete()
    return redirect("student_list")



# @api_view(["GET", "POST"])
# def student_api(request):

#     if request.method == "GET":
#         students = Student.objects.all().order_by("student_id")

#         serializer = StudentSerializer(
#             students,
#             many=True
#         )

#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = StudentSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(
#             serializer.data,
#             status=201
#         )

# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def student_detail_api(request, student_id):

#     student = get_object_or_404(
#         Student,
#         student_id=student_id
#     )

#     if request.method == "GET":
#         serializer = StudentSerializer(student)

#         return Response(serializer.data)

#     if request.method == "PUT":
#         serializer = StudentSerializer(
#             student,
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(serializer.data)

#     if request.method == "PATCH":
#         serializer = StudentSerializer(
#             student,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(serializer.data) 

#     if request.method == "DELETE":
#         student.delete()

#         return Response(
#             status=204
#         )


class StudentViewSet(ModelViewSet):

    queryset = Student.objects.all().order_by("student_id")
    serializer_class = StudentSerializer
    lookup_field = "student_id"
    permission_classes = [IsAuthenticatedReadOnly]