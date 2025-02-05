from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from todo.models import Task

User = get_user_model()


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.task_data = {'title': 'Initial Task', 'description': 'Test Description'}

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass123'})
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.task1 = Task.objects.create(user=self.user, title='Task 1', status='new')
        self.task2 = Task.objects.create(user=self.user, title='Task 2', status='completed')
        self.other_task = Task.objects.create(user=self.other_user, title='Other Task', status='new')

    # Auth
    def test_unauthenticated_access(self):
        self.client.credentials()
        endpoints = [
            '/api/tasks/',
            f'/api/tasks/{self.task1.id}/',
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # CRUD
    def test_create_task(self):
        response = self.client.post('/api/tasks/', self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(response.data['user'], self.user.id)

    def test_retrieve_task(self):
        response = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        updated_data = {'title': 'Updated Task', 'status': 'in_progress'}
        response = self.client.put(f'/api/tasks/{self.task1.id}/', updated_data)
        self.task1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

    # Validation
    def test_title_validation(self):
        invalid_data = {'title': 'A'}
        response = self.client.post('/api/tasks/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Title must be at least 3 characters long.', response.data['title'])

    # File upload
    def test_file_upload(self):
        test_file = SimpleUploadedFile('test_file.txt', b'Test content')
        response = self.client.post('/api/tasks/', {
            'title': 'File Task',
            'file': test_file
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('todo_files/', response.data['file'])

    # Filtering/Search/Ordering
    def test_filter_by_status(self):
        response = self.client.get('/api/tasks/?status=completed')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'completed')

    def test_search_by_title(self):
        response = self.client.get('/api/tasks/?search=Task 1')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task 1')

    def test_ordering(self):
        response = self.client.get('/api/tasks/?ordering=-created_at')
        self.assertEqual(response.data[0]['id'], self.task2.id)

    # Authorization
    def test_access_other_users_task(self):
        response = self.client.get(f'/api/tasks/{self.other_task.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
