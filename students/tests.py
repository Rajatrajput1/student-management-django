from django.test import TestCase
from .models import Student
from .forms import StudentForm
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from students.models import Student

class StudentModelTest(TestCase):

    

    def test_student_creation(self):

        student = Student.objects.create(
            student_id="TEST001",
            name="Test Student",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="test@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        self.assertEqual(student.name, "Test Student")
        self.assertTrue(student.pk)

    def test_invalid_year_range(self):

        form = StudentForm(
            data={
                "student_id": "TEST002",
                "name": "Test Student",
                "date_of_birth": "2000-01-01",
                "contact_number": "9999999999",
                "email": "test2@example.com",
                "course": "B.Tech",
                "start_year": 2026,
                "end_year": 2022,
                "address": "Test Address",
            }
        )

        self.assertFalse(form.is_valid())

        self.assertIn(
            "End year must be greater than or equal to start year.",
            form.non_field_errors()
        )

    def test_valid_year_range(self):

        form = StudentForm(
            data={
                "student_id": "TEST003",
                "name": "Valid Student",
                "date_of_birth": "2000-01-01",
                "contact_number": "9999999999",
                "email": "valid@example.com",
                "course": "B.Tech",
                "start_year": 2022,
                "end_year": 2026,
                "address": "Test Address",
            }
        )

        self.assertTrue(form.is_valid())

class StudentViewTest(TestCase):

    def setUp(self):
            self.user = User.objects.create_user(
                username="testuser",
                password="testpassword123"
                )
    
            self.client.login(
                username="testuser",
                password="testpassword123"
                )

    def test_student_list_view(self):

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "students/student_list.html"
        )

    def test_student_list_contains_student(self):

        student = Student.objects.create(
            student_id="TEST004",
            name="Context Student",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="context@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            student,
            response.context["students"]
        )
    def test_student_edit_returns_404_for_nonexistent_student(self):

        response = self.client.get(
            reverse(
                "student_update",
                args=["DOES_NOT_EXIST"]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_student_create(self):

        data = {
            "student_id": "TEST005",
            "name": "Created Student",
            "date_of_birth": "2000-01-01",
            "contact_number": "9999999999",
            "email": "created@example.com",
            "course": "B.Tech",
            "start_year": 2022,
            "end_year": 2026,
            "address": "Test Address",
        }

        response = self.client.post(
            reverse("student_create"),
            data=data
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Student.objects.filter(
                student_id="TEST005"
            ).exists()
        )

    def test_student_update(self):

        student = Student.objects.create(
            student_id="TEST006",
            name="Original Name",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="original@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Original Address",
        )

        data = {
            "student_id": "TEST006",
            "name": "Updated Name",
            "date_of_birth": "2000-01-01",
            "contact_number": "8888888888",
            "email": "updated@example.com",
            "course": "MBA",
            "start_year": 2023,
            "end_year": 2027,
            "address": "Updated Address",
        }

        response = self.client.post(
            reverse(
                "student_update",
                args=["TEST006"]
            ),
            data=data
        )

        self.assertEqual(response.status_code, 302)

        student.refresh_from_db()

        self.assertEqual(student.name, "Updated Name")
        self.assertEqual(student.course, "MBA")
        self.assertEqual(student.contact_number, "8888888888")

    def test_student_delete_rejects_get(self):

        student = Student.objects.create(
            student_id="TEST007",
            name="Delete Test",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="delete@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        response = self.client.get(
            reverse(
                "student_delete",
                args=["TEST007"]
            )
        )

        self.assertEqual(response.status_code, 405)

        self.assertTrue(
            Student.objects.filter(
                student_id="TEST007"
            ).exists()
        )

    def test_student_delete(self):

        Student.objects.create(
            student_id="TEST008",
            name="Delete Student",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="delete2@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        response = self.client.post(
            reverse(
                "student_delete",
                args=["TEST008"]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Student.objects.filter(
                student_id="TEST008"
            ).exists()
        )

    def test_student_search(self):

        student1 = Student.objects.create(
            student_id="TEST009",
            name="Rajat Kumar",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="rajat@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        student2 = Student.objects.create(
            student_id="TEST010",
            name="Aman Kumar",
            date_of_birth="2000-01-01",
            contact_number="8888888888",
            email="aman@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        response = self.client.get(
            reverse("student_list"),
            {"search": "Rajat"}
        )

        self.assertEqual(response.status_code, 200)

        students = response.context["students"]

        self.assertIn(student1, students)

        self.assertNotIn(student2, students)

    def test_course_filter(self):

        student1 = Student.objects.create(
            student_id="TEST011",
            name="BTech Student",
            date_of_birth="2000-01-01",
            contact_number="9999999999",
            email="btech@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        student2 = Student.objects.create(
            student_id="TEST012",
            name="MBA Student",
            date_of_birth="2000-01-01",
            contact_number="8888888888",
            email="mba@example.com",
            course="MBA",
            start_year=2022,
            end_year=2026,
            address="Test Address",
        )

        response = self.client.get(
            reverse("student_list"),
            {"course": "B.Tech"}
        )

        self.assertEqual(response.status_code, 200)

        students = response.context["students"]

        self.assertIn(student1, students)

        self.assertNotIn(student2, students)

    def test_student_pagination(self):

        for number in range(1, 7):
            Student.objects.create(
                student_id=f"TEST{number:03}",
                name=f"Student {number}",
                date_of_birth="2000-01-01",
                contact_number="9999999999",
                email=f"student{number}@example.com",
                course="B.Tech",
                start_year=2022,
                end_year=2026,
                address="Test Address",
            )

        response_page_1 = self.client.get(
            reverse("student_list"),
            {"page": 1}
        )

        response_page_2 = self.client.get(
            reverse("student_list"),
            {"page": 2}
        )

        students_page_1 = response_page_1.context["students"]
        students_page_2 = response_page_2.context["students"]

        self.assertEqual(students_page_1.number, 1)
        self.assertEqual(students_page_2.number, 2)

        self.assertEqual(len(students_page_1), 5)
        self.assertEqual(len(students_page_2), 1)


class AuthenticationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_login_page(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "students/login.html"
        )

    def test_successful_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword123",
            }
        )

        self.assertRedirects(
            response,
            reverse("student_list")
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_invalid_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "wrongpassword",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_student_list_requires_login(self):
        response = self.client.get(
            reverse("student_list")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_list')}"
        )

    def test_authenticated_user_can_access_student_list(self):
        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        response = self.client.get(
            reverse("student_list")
        )

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        response = self.client.post(
            reverse("logout")
        )

        self.assertRedirects(
            response,
            reverse("login")
        )

        response = self.client.get(
            reverse("student_list")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_list')}"
        )

class StudentAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="apitestuser",
            password="testpassword123"
        )

        self.staff_user = User.objects.create_user(
            username="apistaff",
            password="staffpassword123",
            is_staff=True
        )

        self.client.force_authenticate(user=self.user)

        self.student = Student.objects.create(
            student_id="S10001",
            name="Test Student",
            date_of_birth="2003-01-15",
            contact_number="9876543210",
            email="test@example.com",
            course="B.Tech",
            start_year=2022,
            end_year=2026,
            address="Delhi"
        )

        self.list_url = "/students/api/students/"
        self.detail_url = (
            f"/students/api/students/{self.student.student_id}/"
            )


    def test_list_students(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["student_id"],
            "S10001"
        )

    def test_create_student(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "student_id": "S10002",
            "name": "New Student",
            "date_of_birth": "2004-05-10",
            "contact_number": "9876543211",
            "email": "newstudent@example.com",
            "course": "B.Tech",
            "start_year": 2023,
            "end_year": 2027,
            "address": "Noida"
        }

        response = self.client.post(
            self.list_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.data["student_id"],
            "S10002"
        )

        self.assertTrue(
            Student.objects.filter(
                student_id="S10002"
            ).exists()
        )

    def test_retrieve_student(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.data["student_id"],
            "S10001"
        )

        self.assertEqual(
            response.data["name"],
            "Test Student"
        )
    #PUT
    def test_update_student(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "student_id": "S10001",
            "name": "Updated Student",
            "date_of_birth": "2003-01-15",
            "contact_number": "9999999999",
            "email": "updated@example.com",
            "course": "Computer Science",
            "start_year": 2022,
            "end_year": 2026,
            "address": "Ghaziabad"
        }

        response = self.client.put(
            self.detail_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.data["name"],
            "Updated Student"
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            "Updated Student"
        )
    #PATCH
    def test_partial_update_student(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "name": "Partially Updated Student"
        }

        response = self.client.patch(
            self.detail_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.data["name"],
            "Partially Updated Student"
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            "Partially Updated Student"
        )
    #DELETE

    def test_delete_student(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Student.objects.filter(
                student_id="S10001"
            ).exists()
        )
    #INVALID DATA 
    def test_create_student_with_invalid_years(self):
        self.client.force_authenticate(user=self.staff_user)
        data = {
            "student_id": "S10003",
            "name": "Invalid Student",
            "date_of_birth": "2003-01-15",
            "contact_number": "9876543212",
            "email": "invalid@example.com",
            "course": "B.Tech",
            "start_year": 2026,
            "end_year": 2024,
            "address": "Delhi"
        }

        response = self.client.post(
            self.list_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        self.assertIn(
            "End year must be greater than or equal to start year.",
            str(response.data)
        )

        self.assertFalse(
            Student.objects.filter(
                student_id="S10003"
            ).exists()
        )
    #INVALID STUDENT id
    def test_retrieve_nonexistent_student(self):
        url = "/students/api/students/S99999/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_unauthenticated_user_cannot_access_api(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)

    def test_normal_user_cannot_create_student(self):
        data = {
            "student_id": "S10010",
            "name": "Unauthorized Student",
            "date_of_birth": "2004-01-10",
            "contact_number": "9876543210",
            "email": "unauthorized@example.com",
            "course": "B.Tech",
            "start_year": 2023,
            "end_year": 2027,
            "address": "Delhi"
        }

        response = self.client.post(
            self.list_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Student.objects.filter(
                student_id="S10010"
            ).exists()
        )

    def test_normal_user_cannot_update_student(self):
        data = {
            "student_id": "S10001",
            "name": "Unauthorized Update",
            "date_of_birth": "2003-01-15",
            "contact_number": "9876543210",
            "email": "test@example.com",
            "course": "B.Tech",
            "start_year": 2022,
            "end_year": 2026,
            "address": "Delhi"
        }

        response = self.client.put(
            self.detail_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            "Test Student"
        )

    def test_normal_user_cannot_partial_update_student(self):
        data = {
            "name": "Unauthorized Patch"
        }

        response = self.client.patch(
            self.detail_url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.name,
            "Test Student"
        )

    def test_normal_user_cannot_delete_student(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Student.objects.filter(
                student_id="S10001"
            ).exists()
        )