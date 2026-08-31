[1mdiff --git a/students/forms.py b/students/forms.py[m
[1mindex 3c87534..40578d5 100644[m
[1m--- a/students/forms.py[m
[1m+++ b/students/forms.py[m
[36m@@ -1,7 +1,30 @@[m
 from django import forms[m
 from .models import Student[m
 [m
[32m+[m[32mfrom django import forms[m
[32m+[m[32mfrom .models import Student[m
[32m+[m
[32m+[m
 class StudentForm(forms.ModelForm):[m
[32m+[m
[32m+[m[32m    def clean(self):[m
[32m+[m
[32m+[m[32m        cleaned_data = super().clean()[m
[32m+[m
[32m+[m[32m        start_year = cleaned_data.get("start_year")[m
[32m+[m[32m        end_year = cleaned_data.get("end_year")[m
[32m+[m
[32m+[m[32m        if start_year and end_year:[m
[32m+[m
[32m+[m[32m            if end_year < start_year:[m
[32m+[m[32m                raise forms.ValidationError([m
[32m+[m[32m                    "End year must be greater than or equal to start year."[m
[32m+[m[32m                )[m
[32m+[m
[32m+[m[32m        return cleaned_data[m
[32m+[m
     class Meta:[m
         model = Student[m
[31m-        fields = '__all__'[m
[32m+[m[32m        fields = "__all__"[m
[41m+[m
[41m+[m
[1mdiff --git a/students/static/students/style.css b/students/static/students/style.css[m
[1mindex 452975b..2ea44c1 100644[m
[1m--- a/students/static/students/style.css[m
[1m+++ b/students/static/students/style.css[m
[36m@@ -247,4 +247,47 @@[m [mbody {[m
         align-items: stretch;[m
     }[m
 [m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.pagination {[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    justify-content: center;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m    gap: 8px;[m
[32m+[m[32m    margin-top: 25px;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m
[32m+[m[32m.pagination a,[m
[32m+[m[32m.pagination .current-page {[m
[32m+[m[32m    display: inline-flex;[m
[32m+[m[32m    align-items: center;[m
[32m+[m[32m    justify-content: center;[m
[32m+[m[32m    min-width: 36px;[m
[32m+[m[32m    height: 36px;[m
[32m+[m[32m    padding: 0 10px;[m
[32m+[m[32m    box-sizing: border-box;[m
[32m+[m[32m    border-radius: 7px;[m
[32m+[m[32m    text-decoration: none;[m
[32m+[m[32m    font-size: 14px;[m
[32m+[m[32m    font-weight: 600;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m
[32m+[m[32m.pagination a {[m
[32m+[m[32m    color: #2563eb;[m
[32m+[m[32m    background-color: white;[m
[32m+[m[32m    border: 1px solid #d1d5db;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m
[32m+[m[32m.pagination a:hover {[m
[32m+[m[32m    background-color: #eff6ff;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m
[32m+[m[32m.pagination .current-page {[m
[32m+[m[32m    color: white;[m
[32m+[m[32m    background-color: #2563eb;[m
[32m+[m[32m    border: 1px solid #2563eb;[m
 }[m
\ No newline at end of file[m
[1mdiff --git a/students/templates/students/student_list.html b/students/templates/students/student_list.html[m
[1mindex cecead4..a1c5328 100644[m
[1m--- a/students/templates/students/student_list.html[m
[1m+++ b/students/templates/students/student_list.html[m
[36m@@ -48,6 +48,45 @@[m
       </form>[m
       <div class = "table-container">[m
         <table class="student-table">[m
[32m+[m[32m            {% if students.paginator.num_pages > 1 %}[m
[32m+[m
[32m+[m[32m<div class="pagination">[m
[32m+[m
[32m+[m[32m    {% if students.has_previous %}[m
[32m+[m[32m        <a href="?{{ query_params.urlencode }}&page={{ students.previous_page_number }}">[m
[32m+[m[32m            ← Previous[m
[32m+[m[32m        </a>[m
[32m+[m[32m    {% endif %}[m
[32m+[m
[32m+[m
[32m+[m[32m    {% for page_num in students.paginator.page_range %}[m
[32m+[m
[32m+[m[32m        {% if students.number == page_num %}[m
[32m+[m
[32m+[m[32m            <span class="current-page">[m
[32m+[m[32m                {{ page_num }}[m
[32m+[m[32m            </span>[m
[32m+[m
[32m+[m[32m        {% else %}[m
[32m+[m
[32m+[m[32m            <a href="?{{ query_params.urlencode }}&page={{ page_num }}">[m
[32m+[m[32m                {{ page_num }}[m
[32m+[m[32m            </a>[m
[32m+[m
[32m+[m[32m        {% endif %}[m
[32m+[m
[32m+[m[32m    {% endfor %}[m
[32m+[m
[32m+[m
[32m+[m[32m    {% if students.has_next %}[m
[32m+[m[32m        <a href="?{{ query_params.urlencode }}&page={{ students.next_page_number }}">[m
[32m+[m[32m            Next →[m
[32m+[m[32m        </a>[m
[32m+[m[32m    {% endif %}[m
[32m+[m
[32m+[m[32m</div>[m
[32m+[m
[32m+[m[32m{% endif %}[m
             <tr>[m
             <th>Student ID</th>[m
             <th>Name</th>[m
[1mdiff --git a/students/tests.py b/students/tests.py[m
[1mindex 7ce503c..07f2a4c 100644[m
[1m--- a/students/tests.py[m
[1m+++ b/students/tests.py[m
[36m@@ -1,3 +1,353 @@[m
 from django.test import TestCase[m
[32m+[m[32mfrom .models import Student[m
[32m+[m[32mfrom .forms import StudentForm[m
[32m+[m[32mfrom django.urls import reverse[m
 [m
[31m-# Create your tests here.[m
[32m+[m[32mclass StudentModelTest(TestCase):[m
[32m+[m
[32m+[m[32m    def test_student_creation(self):[m
[32m+[m
[32m+[m[32m        student = Student.objects.create([m
[32m+[m[32m            student_id="TEST001",[m
[32m+[m[32m            name="Test Student",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="test@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(student.name, "Test Student")[m
[32m+[m[32m        self.assertTrue(student.pk)[m
[32m+[m
[32m+[m[32m    def test_invalid_year_range(self):[m
[32m+[m
[32m+[m[32m        form = StudentForm([m
[32m+[m[32m            data={[m
[32m+[m[32m                "student_id": "TEST002",[m
[32m+[m[32m                "name": "Test Student",[m
[32m+[m[32m                "date_of_birth": "2000-01-01",[m
[32m+[m[32m                "contact_number": "9999999999",[m
[32m+[m[32m                "email": "test2@example.com",[m
[32m+[m[32m                "course": "B.Tech",[m
[32m+[m[32m                "start_year": 2026,[m
[32m+[m[32m                "end_year": 2022,[m
[32m+[m[32m                "address": "Test Address",[m
[32m+[m[32m            }[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertFalse(form.is_valid())[m
[32m+[m
[32m+[m[32m        self.assertIn([m
[32m+[m[32m            "End year must be greater than or equal to start year.",[m
[32m+[m[32m            form.non_field_errors()[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    def test_valid_year_range(self):[m
[32m+[m
[32m+[m[32m        form = StudentForm([m
[32m+[m[32m            data={[m
[32m+[m[32m                "student_id": "TEST003",[m
[32m+[m[32m                "name": "Valid Student",[m
[32m+[m[32m                "date_of_birth": "2000-01-01",[m
[32m+[m[32m                "contact_number": "9999999999",[m
[32m+[m[32m                "email": "valid@example.com",[m
[32m+[m[32m                "course": "B.Tech",[m
[32m+[m[32m                "start_year": 2022,[m
[32m+[m[32m                "end_year": 2026,[m
[32m+[m[32m                "address": "Test Address",[m
[32m+[m[32m            }[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertTrue(form.is_valid())[m
[32m+[m
[32m+[m[32mclass StudentViewTest(TestCase):[m
[32m+[m
[32m+[m[32m    def test_student_list_view(self):[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse("student_list")[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 200)[m
[32m+[m
[32m+[m[32m        self.assertTemplateUsed([m
[32m+[m[32m            response,[m
[32m+[m[32m            "students/student_list.html"[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    def test_student_list_contains_student(self):[m
[32m+[m
[32m+[m[32m        student = Student.objects.create([m
[32m+[m[32m            student_id="TEST004",[m
[32m+[m[32m            name="Context Student",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="context@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse("student_list")[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 200)[m
[32m+[m
[32m+[m[32m        self.assertIn([m
[32m+[m[32m            student,[m
[32m+[m[32m            response.context["students"][m
[32m+[m[32m        )[m
[32m+[m[32m    def test_student_edit_returns_404_for_nonexistent_student(self):[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse([m
[32m+[m[32m                "student_update",[m
[32m+[m[32m                args=["DOES_NOT_EXIST"][m
[32m+[m[32m            )[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 404)[m
[32m+[m
[32m+[m[32m    def test_student_create(self):[m
[32m+[m
[32m+[m[32m        data = {[m
[32m+[m[32m            "student_id": "TEST005",[m
[32m+[m[32m            "name": "Created Student",[m
[32m+[m[32m            "date_of_birth": "2000-01-01",[m
[32m+[m[32m            "contact_number": "9999999999",[m
[32m+[m[32m            "email": "created@example.com",[m
[32m+[m[32m            "course": "B.Tech",[m
[32m+[m[32m            "start_year": 2022,[m
[32m+[m[32m            "end_year": 2026,[m
[32m+[m[32m            "address": "Test Address",[m
[32m+[m[32m        }[m
[32m+[m
[32m+[m[32m        response = self.client.post([m
[32m+[m[32m            reverse("student_create"),[m
[32m+[m[32m            data=data[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 302)[m
[32m+[m
[32m+[m[32m        self.assertTrue([m
[32m+[m[32m            Student.objects.filter([m
[32m+[m[32m                student_id="TEST005"[m
[32m+[m[32m            ).exists()[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    def test_student_update(self):[m
[32m+[m
[32m+[m[32m        student = Student.objects.create([m
[32m+[m[32m            student_id="TEST006",[m
[32m+[m[32m            name="Original Name",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="original@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Original Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        data = {[m
[32m+[m[32m            "student_id": "TEST006",[m
[32m+[m[32m            "name": "Updated Name",[m
[32m+[m[32m            "date_of_birth": "2000-01-01",[m
[32m+[m[32m            "contact_number": "8888888888",[m
[32m+[m[32m            "email": "updated@example.com",[m
[32m+[m[32m            "course": "MBA",[m
[32m+[m[32m            "start_year": 2023,[m
[32m+[m[32m            "end_year": 2027,[m
[32m+[m[32m            "address": "Updated Address",[m
[32m+[m[32m        }[m
[32m+[m
[32m+[m[32m        response = self.client.post([m
[32m+[m[32m            reverse([m
[32m+[m[32m                "student_update",[m
[32m+[m[32m                args=["TEST006"][m
[32m+[m[32m            ),[m
[32m+[m[32m            data=data[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 302)[m
[32m+[m
[32m+[m[32m        student.refresh_from_db()[m
[32m+[m
[32m+[m[32m        self.assertEqual(student.name, "Updated Name")[m
[32m+[m[32m        self.assertEqual(student.course, "MBA")[m
[32m+[m[32m        self.assertEqual(student.contact_number, "8888888888")[m
[32m+[m
[32m+[m[32m    def test_student_delete_rejects_get(self):[m
[32m+[m
[32m+[m[32m        student = Student.objects.create([m
[32m+[m[32m            student_id="TEST007",[m
[32m+[m[32m            name="Delete Test",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="delete@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse([m
[32m+[m[32m                "student_delete",[m
[32m+[m[32m                args=["TEST007"][m
[32m+[m[32m            )[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 405)[m
[32m+[m
[32m+[m[32m        self.assertTrue([m
[32m+[m[32m            Student.objects.filter([m
[32m+[m[32m                student_id="TEST007"[m
[32m+[m[32m            ).exists()[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    def test_student_delete(self):[m
[32m+[m
[32m+[m[32m        Student.objects.create([m
[32m+[m[32m            student_id="TEST008",[m
[32m+[m[32m            name="Delete Student",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="delete2@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response = self.client.post([m
[32m+[m[32m            reverse([m
[32m+[m[32m                "student_delete",[m
[32m+[m[32m                args=["TEST008"][m
[32m+[m[32m            )[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 302)[m
[32m+[m
[32m+[m[32m        self.assertFalse([m
[32m+[m[32m            Student.objects.filter([m
[32m+[m[32m                student_id="TEST008"[m
[32m+[m[32m            ).exists()[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m    def test_student_search(self):[m
[32m+[m
[32m+[m[32m        student1 = Student.objects.create([m
[32m+[m[32m            student_id="TEST009",[m
[32m+[m[32m            name="Rajat Kumar",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="rajat@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        student2 = Student.objects.create([m
[32m+[m[32m            student_id="TEST010",[m
[32m+[m[32m            name="Aman Kumar",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="8888888888",[m
[32m+[m[32m            email="aman@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse("student_list"),[m
[32m+[m[32m            {"search": "Rajat"}[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 200)[m
[32m+[m
[32m+[m[32m        students = response.context["students"][m
[32m+[m
[32m+[m[32m        self.assertIn(student1, students)[m
[32m+[m
[32m+[m[32m        self.assertNotIn(student2, students)[m
[32m+[m
[32m+[m[32m    def test_course_filter(self):[m
[32m+[m
[32m+[m[32m        student1 = Student.objects.create([m
[32m+[m[32m            student_id="TEST011",[m
[32m+[m[32m            name="BTech Student",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="9999999999",[m
[32m+[m[32m            email="btech@example.com",[m
[32m+[m[32m            course="B.Tech",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        student2 = Student.objects.create([m
[32m+[m[32m            student_id="TEST012",[m
[32m+[m[32m            name="MBA Student",[m
[32m+[m[32m            date_of_birth="2000-01-01",[m
[32m+[m[32m            contact_number="8888888888",[m
[32m+[m[32m            email="mba@example.com",[m
[32m+[m[32m            course="MBA",[m
[32m+[m[32m            start_year=2022,[m
[32m+[m[32m            end_year=2026,[m
[32m+[m[32m            address="Test Address",[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response = self.client.get([m
[32m+[m[32m            reverse("student_list"),[m
[32m+[m[32m            {"course": "B.Tech"}[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        self.assertEqual(response.status_code, 200)[m
[32m+[m
[32m+[m[32m        students = response.context["students"][m
[32m+[m
[32m+[m[32m        self.assertIn(student1, students)[m
[32m+[m
[32m+[m[32m        self.assertNotIn(student2, students)[m
[32m+[m
[32m+[m[32m    def test_student_pagination(self):[m
[32m+[m
[32m+[m[32m        for number in range(1, 7):[m
[32m+[m[32m            Student.objects.create([m
[32m+[m[32m                student_id=f"TEST{number:03}",[m
[32m+[m[32m                name=f"Student {number}",[m
[32m+[m[32m                date_of_birth="2000-01-01",[m
[32m+[m[32m                contact_number="9999999999",[m
[32m+[m[32m                email=f"student{number}@example.com",[m
[32m+[m[32m                course="B.Tech",[m
[32m+[m[32m                start_year=2022,[m
[32m+[m[32m                end_year=2026,[m
[32m+[m[32m                address="Test Address",[m
[32m+[m[32m            )[m
[32m+[m
[32m+[m[32m        response_page_1 = self.client.get([m
[32m+[m[32m            reverse("student_list"),[m
[32m+[m[32m            {"page": 1}[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        response_page_2 = self.client.get([m
[32m+[m[32m            reverse("student_list"),[m
[32m+[m[32m            {"page": 2}[m
[32m+[m[32m        )[m
[32m+[m
[32m+[m[32m        students_page_1 = response_page_1.context["students"][m
[32m+[m[32m        students_page_2 = response_page_2.context["students"][m
[32m+[m
[32m+[m[32m        self.assertEqual(students_page_1.number, 1)[m
[32m+[m[32m        self.assertEqual(students_page_2.number, 2)[m
[32m+[m
[32m+[m[32m        self.assertEqual(len(students_page_1), 5)[m
[32m+[m[32m        self.assertEqual(len(students_page_2), 1)[m
\ No newline at end of file[m
[1mdiff --git a/students/views.py b/students/views.py[m
[1mindex fd35f3c..ccb95b4 100644[m
[1m--- a/students/views.py[m
[1m+++ b/students/views.py[m
[36m@@ -6,7 +6,7 @@[m [mfrom .forms import StudentForm[m
 [m
 # Create your views here.[m
 def student_list(request):[m
[31m-    students = Student.objects.all()[m
[32m+[m[32m    students = Student.objects.all().order_by("student_id")[m
 [m
     search = request.GET.get('search')[m
     if search:[m
[36m@@ -25,15 +25,19 @@[m [mdef student_list(request):[m
                 flat=True[m
             ).distinct()[m
 [m
[31m-    paginator = Paginator(students,10)[m
[32m+[m[32m    paginator = Paginator(students,5)[m
     page_number = request.GET.get("page")[m
     page_obj = paginator.get_page(page_number)[m
[32m+[m
[32m+[m[32m    query_params = request.GET.copy()[m
[32m+[m[32m    query_params.pop("page", None)[m
     [m
     return render([m
         request,[m
         "students/student_list.html",[m
         {[m
             "students" : page_obj,[m
[32m+[m[32m            "query_params": query_params,[m
             "courses" : courses,[m
             "search": search,[m
             "course": course[m
