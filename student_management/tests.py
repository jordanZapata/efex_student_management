from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Student

class StudentTests(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="2000-01-15",
            grade=10,
            phone="+123456789",
            email="john@example.com"
        )
        self.list_url = reverse('student-list-create')
        self.detail_url = reverse('student-detail', args=[self.student.id])

    def test_create_student(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1998-05-20",
            "grade": 11,
            "phone": "+987654321",
            "email": "jane@example.com"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_retrieve_student(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_update_student(self):
        updated_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1998-05-20",
            "grade": 11,
            "phone": "+987654321",
            "email": "jane@example.com"
        }
        response = self.client.patch(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')

        # Refresh the student instance from the database
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Jane')
