"""
Sample tests សម្រាប់ Task API។
រត់ដោយប្រើ command: python manage.py test
"""
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        # បង្កើត user សម្រាប់សាកល្បង authenticated requests (POST/PUT/DELETE)
        self.user = User.objects.create_user(username='tester', password='pass12345')

        self.task1 = Task.objects.create(
            title='Buy groceries',
            description='Milk, eggs, bread',
            priority=Task.Priority.LOW,
        )
        self.task2 = Task.objects.create(
            title='Finish Django project',
            description='Deploy to Render with PostgreSQL',
            priority=Task.Priority.HIGH,
        )
        self.list_url = reverse('task-list')

    # ---------- Read-only endpoints: no auth required ----------
    def test_list_tasks_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_single_task(self):
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Buy groceries')

    def test_filter_by_priority(self):
        response = self.client.get(self.list_url, {'priority': 'HIGH'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Finish Django project')

    def test_search_tasks(self):
        response = self.client.get(self.list_url, {'search': 'Render'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    # ---------- Write endpoints: require authentication ----------
    def test_create_task_requires_authentication(self):
        payload = {'title': 'Unauthenticated attempt', 'priority': 'LOW'}
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_authenticated(self):
        self.client.login(username='tester', password='pass12345')
        payload = {
            'title': 'Write documentation',
            'description': 'Explain how to test with Postman',
            'priority': 'MEDIUM',
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Write documentation')

    def test_create_task_blank_title_fails_validation(self):
        self.client.login(username='tester', password='pass12345')
        response = self.client.post(self.list_url, {'title': '   '})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task(self):
        self.client.login(username='tester', password='pass12345')
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.patch(url, {'is_completed': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)

    def test_delete_task(self):
        self.client.login(username='tester', password='pass12345')
        url = reverse('task-detail', args=[self.task2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_health_check_endpoint(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'ok')

    def test_homepage_renders_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'Task API', response.content)
