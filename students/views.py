from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Student
from .forms import StudentForm

# Create your views here.
def student_list(request):
    students = Student.objects.all()

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

    paginator = Paginator(students,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        "students/student_list.html",
        {
            "students" : page_obj,
            "courses" : courses,
            "search": search,
            "course": course
        }

    )

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
@require_POST

def student_delete(request, student_id):
    student = get_object_or_404(
        Student,
        student_id=student_id
    )

    student.delete()
    return redirect("student_list")
