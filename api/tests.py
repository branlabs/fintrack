from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User, Category
from api.v1.serializers import UserSerializer, CategorySerializer


class Patch1ValidationTests(APITestCase):
    def test_user_serializer_contract_exposes_only_id_and_name(self):
        serializer = UserSerializer()
        self.assertEqual(list(serializer.fields.keys()), ['id', 'name'])
        self.assertTrue(serializer.fields['id'].read_only)

    def test_category_serializer_contract_exposes_only_id_and_name(self):
        serializer = CategorySerializer()
        self.assertEqual(list(serializer.fields.keys()), ['id', 'name'])
        self.assertTrue(serializer.fields['id'].read_only)

    def test_user_create_invalid_payload_returns_400(self):
        response = self.client.post(reverse('user-list'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_create_invalid_payload_still_returns_400_after_modelserializer_change(self):
        response = self.client.post(reverse('user-list'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_create_invalid_payload_returns_400(self):
        response = self.client.post(reverse('category-list'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_category_create_invalid_payload_still_returns_400_after_modelserializer_change(self):
        response = self.client.post(reverse('category-list'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update_invalid_payload_returns_400(self):
        user = User.objects.create(name='Existing User')
        response = self.client.put(reverse('user-detail', args=[user.pk]), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_category_update_invalid_payload_returns_400(self):
        category = Category.objects.create(name='Existing Category')
        response = self.client.put(reverse('category-detail', args=[category.pk]), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_create_valid_payload_returns_201(self):
        response = self.client.post(
            reverse('user-list'),
            {'name': 'New User'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'New User')
        self.assertIn('id', response.data)

    def test_category_create_valid_payload_returns_201(self):
        response = self.client.post(
            reverse('category-list'),
            {'name': 'New Category'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), 'New Category')
        self.assertIn('id', response.data)

    def test_user_duplicate_name_returns_400(self):
        User.objects.create(name='Duplicate User')
        response = self.client.post(
            reverse('user-list'),
            {'name': 'Duplicate User'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_category_duplicate_name_returns_400(self):
        Category.objects.create(name='Duplicate Category')
        response = self.client.post(
            reverse('category-list'),
            {'name': 'Duplicate Category'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)


class Patch1NotFoundTests(APITestCase):
    def test_user_get_not_found_returns_404(self):
        url = reverse('user-detail', args=[999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_put_not_found_returns_404(self):
        url = reverse('user-detail', args=[999999])
        response = self.client.put(url, {'name': 'Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_delete_not_found_returns_404(self):
        url = reverse('user-detail', args=[999999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_get_not_found_returns_404(self):
        url = reverse('category-detail', args=[999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_put_not_found_returns_404(self):
        url = reverse('category-detail', args=[999999])
        response = self.client.put(url, {'name': 'Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_delete_not_found_returns_404(self):
        url = reverse('category-detail', args=[999999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Patch2SummaryValidationTests(APITestCase):
    def test_summary_day_invalid_month_out_of_range_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'day', 'year': '2025', 'month': '13'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid month')

    def test_summary_day_invalid_month_non_integer_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'day', 'year': '2025', 'month': 'abc'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid month')

    def test_summary_month_invalid_year_non_integer_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'month', 'year': 'abc'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid year')

    def test_summary_month_valid_input_returns_200(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'month', 'year': '2025'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('group'), 'month')
        self.assertIn('data', response.data)

    def test_summary_week_invalid_year_non_integer_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'week', 'year': 'abc', 'month': '5'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid year')

    def test_summary_week_invalid_month_non_integer_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'week', 'year': '2025', 'month': 'abc'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid month')

    def test_summary_year_invalid_year_non_integer_returns_400(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'year', 'year': 'abc'},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('detail'), 'invalid year')

    def test_summary_year_valid_input_returns_200(self):
        response = self.client.get(
            reverse('transaction-summary'),
            {'group': 'year', 'year': '2025'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('group'), 'year')
        self.assertIn('data', response.data)
