from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Item
from .services import create_item
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache


class ItemAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = AccessToken.for_user(self.user)
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"

    def tearDown(self):
        cache.clear()

    def test_create_item(self):
        """Test creating a new item."""
        data = {
            "name": "Test Item",
            "description": "A test item description.",
            "quantity": 10,
        }
        response = self.client.post(reverse("create_item"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

    def test_create_duplicate_item(self):

        create_item(
            {
                "name": "Test Item",
                "description": "A test item description.",
                "quantity": 10,
            }
        )
        data = {
            "name": "Test Item",
            "description": "Another test item description.",
            "quantity": 5,
        }
        response = self.client.post(reverse("create_item"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "An item with the name 'Test Item' already exists.",
            str(response.data["message"]),
        )

    def test_read_item(self):

        item = create_item(
            {
                "name": "Test Item",
                "description": "A test item description.",
                "quantity": 10,
            }
        )
        response = self.client.get(reverse("item", args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "Test Item")

    def test_update_item(self):

        item = create_item(
            {
                "name": "Test Item",
                "description": "A test item description.",
                "quantity": 10,
            }
        )
        data = {
            "name": "Updated Item",
            "description": "Updated description.",
            "quantity": 15,
        }
        response = self.client.put(reverse("item", args=[item.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, "Updated Item")

    def test_delete_item(self):

        item = create_item(
            {
                "name": "Test Item",
                "description": "A test item description.",
                "quantity": 10,
            }
        )
        response = self.client.delete(reverse("item", args=[item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_read_nonexistent_item(self):
        response = self.client.get(reverse("item", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Item does not exis", str(response.data["message"]))
