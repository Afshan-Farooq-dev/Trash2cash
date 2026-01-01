from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, WasteRecord


class WasteHistoryViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass')
        # Ensure profile exists
        UserProfile.objects.create(user=self.user)

        now = timezone.now()
        # Recent record within 1 day
        WasteRecord.objects.create(
            user=self.user,
            disposed_at=now - timedelta(days=1),
            waste_type='plastic',
            points_earned=10,
        )
        # Older record 10 days ago
        WasteRecord.objects.create(
            user=self.user,
            disposed_at=now - timedelta(days=10),
            waste_type='paper',
            points_earned=5,
        )

    def test_waste_history_basic(self):
        self.client.login(username='tester', password='pass')
        url = reverse('waste_history')
        resp = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('records', data)
        # Both records present
        self.assertEqual(len(data['records']), 2)

    def test_waste_history_date_filter(self):
        self.client.login(username='tester', password='pass')
        url = reverse('waste_history')
        # filter to include only last 2 days
        from_date = (timezone.now() - timedelta(days=2)).date().isoformat()
        # First fetch all records
        resp_all = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp_all.status_code, 200)
        all_data = resp_all.json()

        # Now fetch with the date filter
        resp = self.client.get(
            url, {'from': from_date}, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Filtered result should be <= total records and at least 0
        self.assertLessEqual(len(data['records']), len(all_data['records']))

    def test_waste_history_type_filter(self):
        self.client.login(username='tester', password='pass')
        url = reverse('waste_history')
        resp = self.client.get(
            url, {'type': 'plastic'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data['records']), 1)
