# api/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Wine


class WineAPITests(APITestCase):
    def setUp(self):
        # Clean up any existing data
        Wine.objects.all().delete()
        
        # Verify it's really clean
        self.assertEqual(Wine.objects.count(), 0, "Database was not clean before creating test wines!")
        
        # Now create the two test wines
        Wine.objects.create(
            type='red',
            fixed_acidity=7.4,
            volatile_acidity=0.7,
            citric_acid=0.0,
            residual_sugar=1.9,
            chlorides=0.076,
            free_sulfur_dioxide=11.0,
            total_sulfur_dioxide=34.0,
            density=0.9978,
            pH=3.51,
            sulphates=0.56,
            alcohol=9.4,
            quality=5
        )
        Wine.objects.create(
            type='white',
            fixed_acidity=6.3,
            volatile_acidity=0.3,
            citric_acid=0.34,
            residual_sugar=1.6,
            chlorides=0.049,
            free_sulfur_dioxide=14.0,
            total_sulfur_dioxide=132.0,
            density=0.9940,
            pH=3.30,
            sulphates=0.49,
            alcohol=9.5,
            quality=6
        )
        
        self.client = APIClient()
        
        # Final check
        self.assertEqual(Wine.objects.count(), 2)

    def test_list_wines(self):
        url = reverse('wine-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Access the paginated results
        self.assertEqual(len(response.data['results']), 2)

    def test_retrieve_single_wine(self):
        wine = Wine.objects.first()
        url = reverse('wine-detail', kwargs={'pk': wine.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quality'], wine.quality)

    def test_create_wine_via_post(self):
        url = reverse('wine-list')
        data = {
            "type": "red",
            "fixed_acidity": 8.5,
            "volatile_acidity": 0.28,
            "citric_acid": 0.56,
            "residual_sugar": 2.1,
            "chlorides": 0.081,
            "free_sulfur_dioxide": 15.0,
            "total_sulfur_dioxide": 45.0,
            "density": 0.996,
            "pH": 3.25,
            "sulphates": 0.68,
            "alcohol": 11.2,
            "quality": 7
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wine.objects.count(), 3)

    def test_filter_by_type(self):
        url = reverse('wine-list') + '?type=white'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Access the paginated results
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'white')