from django.test import TestCase
from .models import Student
from .forms import StudentForm
from django.urls import reverse

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