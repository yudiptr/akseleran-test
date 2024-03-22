from django.test import TestCase
from .models import KYCUsers
from django.test import RequestFactory
from django.urls import reverse
from .views import KYCUserViewSet

class KYCUsersTestCase(TestCase):
    def setUp(self):
        self.user = KYCUsers.objects.create(
            user_id='123',
            name='Test User',
            phone_number='+1234567890',
            email='test@example.com',
            address='Test Address',
            city='Test City',
            zip_code='12345',
            occupation='Test Occupation',
            monthly_income=5000.00,
            isVerified=False
        )

    def test_user_creation(self):
        """Test the creation of a KYC user"""
        self.assertEqual(self.user.user_id, '123')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.phone_number, '+1234567890')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.address, 'Test Address')
        self.assertEqual(self.user.city, 'Test City')
        self.assertEqual(self.user.zip_code, '12345')
        self.assertEqual(self.user.occupation, 'Test Occupation')
        self.assertEqual(self.user.monthly_income, 5000.00)
        self.assertFalse(self.user.isVerified)

class KYCUserViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = KYCUsers.objects.create(
            user_id='123',
            name='Test User',
            phone_number='+1234567890',
            email='test@example.com',
            address='Test Address',
            city='Test City',
            zip_code='12345',
            occupation='Test Occupation',
            monthly_income=5000.00,
            isVerified=False
        )

    def test_list_users(self):
        """Test the list users API endpoint"""
        view = KYCUserViewSet.as_view({'get': 'list'})
        request = self.factory.get('/users/')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_user_id(self):
        """Test the filter by user_id API endpoint"""
        view = KYCUserViewSet.as_view({'get': 'filter_by_user_id'})
        request = self.factory.get('/users/filter_by_user_id/?user_id=123')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            "user_id": "123",
            "name": "Test User",
            "phone_number": "+1234567890",
            "email": "test@example.com",
            "address": "Test Address",
            "city": "Test City",
            "zip_code": "12345",
            "occupation": "Test Occupation",
            "monthly_income": '5000.00',
            "isVerified": False,
            'email_before_update': None, 
            'phone_number_before_update': None
        })

    def test_filter_by_admin(self):
        """Test the list users API endpoint"""
        view = KYCUserViewSet.as_view({'get': 'admin_view'})
        request = self.factory.get('/users/admin_view')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            "user_id": "123",
            "name": "Test User",
            "phone_number": "+1234567890",
            "email": "test@example.com",
            "address": "Test Address",
            "city": "Test City",
            "zip_code": "12345",
            'email_before_update': None, 
            'phone_number_before_update': None
        })

    def test_update_user(self):
        self.user.name = 'Updated Test User'
        self.user.phone_number = '+9876543210'
        self.user.email = 'updated_test@example.com'
        self.user.address = 'Updated Test Address'
        self.user.city = 'Updated Test City'
        self.user.zip_code = '54321'
        self.user.occupation = 'Updated Test Occupation'
        self.user.monthly_income = 6000.00
        self.user.isVerified = True
        self.user.save()

        updated_user = KYCUsers.objects.get(user_id='123')

        self.assertEqual(updated_user.name, 'Updated Test User')
        self.assertEqual(updated_user.phone_number, '+9876543210')
        self.assertEqual(updated_user.email, 'updated_test@example.com')
        self.assertEqual(updated_user.address, 'Updated Test Address')
        self.assertEqual(updated_user.city, 'Updated Test City')
        self.assertEqual(updated_user.zip_code, '54321')
        self.assertEqual(updated_user.occupation, 'Updated Test Occupation')
        self.assertAlmostEqual(updated_user.monthly_income, 6000.00)
        self.assertTrue(updated_user.isVerified)