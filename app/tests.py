from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User


class APITestCase(TestCase):
    def setUp(self):
        self.username = 'anirudh'
        self.password = '87654321'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='TEST001')
        self.purchase_order = PurchaseOrder.objects.create(po_number='PO001', vendor=self.vendor, order_date='2024-01-01', delivery_date='2024-01-10', items={}, quantity=1, status='completed', issue_date='2024-01-01', acknowledgment_date='2024-01-02')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_vendor_list_create_endpoint(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': 'NEW001'
        }
        response = self.client.post('/api/vendors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vendor.objects.filter(name='New Vendor').exists())

    def test_vendor_retrieve_update_destroy_endpoint(self):
        response = self.client.get(f'/api/vendors/{self.vendor.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated Contact',
            'address': 'Updated Address',
            'vendor_code': 'UPDATED001'
        }
        response = self.client.put(f'/api/vendors/{self.vendor.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'Updated Vendor')
        response = self.client.delete(f'/api/vendors/{self.vendor.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(pk=self.vendor.pk).exists())

    def test_purchase_order_list_create_endpoint(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'po_number': 'PO002',
            'vendor': self.vendor.pk,
            'order_date': '2024-02-01',
            'delivery_date': '2024-02-10',
            'items': {},
            'quantity': 1,
            'status': 'completed',
            'issue_date': '2024-02-01',
            'acknowledgment_date': '2024-02-02'
        }
        response = self.client.post('/api/purchase_orders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PurchaseOrder.objects.filter(po_number='PO002').exists())

    def test_purchase_order_retrieve_update_destroy_endpoint(self):
        response = self.client.get(f'/api/purchase_orders/{self.purchase_order.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'po_number': 'PO003',
            'vendor': self.vendor.pk,
            'order_date': '2024-03-01',
            'delivery_date': '2024-03-10',
            'items': {},
            'quantity': 1,
            'status': 'completed',
            'issue_date': '2024-03-01',
            'acknowledgment_date': '2024-03-02'
        }
        response = self.client.put(f'/api/purchase_orders/{self.purchase_order.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, 'PO003')
        response = self.client.delete(f'/api/purchase_orders/{self.purchase_order.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PurchaseOrder.objects.filter(pk=self.purchase_order.pk).exists())

    def test_vendor_performance_endpoint(self):
        response = self.client.get(f'/api/vendors/{self.vendor.pk}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
