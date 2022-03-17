from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientAPITest:
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest:
    """Test taht ingredients can be accessed by authorized user"""

    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            "test@foobar.com", "pass123"
        )
        self.client.force_authenticate(user)

    def test_retrieve_ingredients_successful(self):
        Ingredient.objects.create(user=self.user, name="Carrots")
        Ingredient.objects.create(user=self.user, name="Peas")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serizalizer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serizalizer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            "user2@foobar.com", "pas1234"
        )
        Ingredient.objects.create(user=user2, name="Spice")
        ingredient = Ingredient.objects.create(user=self.user, name="Sand")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
