from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from todo.models import Task, Comment

User = get_user_model()


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')

        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass123'})
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.task = Task.objects.create(user=self.user, title='Main Task')
        self.comment = Comment.objects.create(task=self.task, user=self.user, text='Initial comment')
        self.other_task = Task.objects.create(user=self.other_user, title='Other Task')

    # CRUD
    def test_create_comment(self):
        response = self.client.post(f'/api/tasks/{self.task.id}/comments/', {'text': 'New comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_retrieve_comment(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Initial comment')

    def test_update_comment(self):
        response = self.client.put(
            f'/api/tasks/{self.task.id}/comments/{self.comment.id}/',
            {'text': 'Updated comment'}
        )
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.text, 'Updated comment')

    def test_delete_comment(self):
        response = self.client.delete(f'/api/tasks/{self.task.id}/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    # Negative
    def test_invalid_task_comment_creation(self):
        response = self.client.post('/api/tasks/999/comments/', {'text': 'Invalid comment'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
