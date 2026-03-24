import json
from django.test import TestCase, Client
from contact.models import ContactMessage


class ContactModelTest(TestCase):
    """Test the ContactMessage model."""

    def test_create_message(self):
        msg = ContactMessage.objects.create(
            name="John", email="john@example.com", message="Hello!"
        )
        self.assertEqual(msg.name, "John")
        self.assertEqual(msg.email, "john@example.com")
        self.assertEqual(str(msg), f"John - john@example.com ({msg.created_at:%Y-%m-%d %H:%M})")

    def test_ordering(self):
        msg1 = ContactMessage.objects.create(name="A", email="a@test.com", message="First")
        msg2 = ContactMessage.objects.create(name="B", email="b@test.com", message="Second")
        messages = list(ContactMessage.objects.all())
        self.assertEqual(messages[0].name, "B")  # Newest first


class ContactViewTest(TestCase):
    """Test the contact form submission endpoint."""

    def setUp(self):
        self.client = Client()
        self.url = '/contact/submit/'

    def test_valid_submission(self):
        response = self.client.post(self.url,
            data=json.dumps({"name": "Test", "email": "test@test.com", "message": "Hi"}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_missing_fields(self):
        response = self.client.post(self.url,
            data=json.dumps({"name": "", "email": "test@test.com", "message": "Hi"}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_invalid_json(self):
        response = self.client.post(self.url,
            data="not json",
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'RAGHAVARAJAN')
