from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientAPITest(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test taht ingredients can be accessed by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@foobar.com", "pass123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_successful(self):
        """Test that the ingredients are retrievable after creation"""
        Ingredient.objects.create(user=self.user, name="Carrots")
        Ingredient.objects.create(user=self.user, name="Peas")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serizalizer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serizalizer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_user(self):
        """ "Test that only the ingredients of the authed user are returned"""
        user2 = get_user_model().objects.create_user(
            "user2@foobar.com", "pas1234"
        )
        Ingredient.objects.create(user=user2, name="Spice")
        ingredient = Ingredient.objects.create(user=self.user, name="Sand")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredients_succesful(self):
        """Test that creating an ingredient succeeds"""
        payload = {"name": "cabbage"}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user, name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredients_invalid(self):
        """Test that invalid ingredients name won't be created"""
        payload = {"name": ""}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
