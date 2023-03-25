from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from pereval.test_json import DATA


class SubmitDataTest(APITestCase):
    def test_get_data(self):
        url = reverse('submitdata')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('submitdata')
        data = DATA
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data, {'status': 200, 'message': None, 'id': 1})


    # def test_get_detail(self):
    #     url = reverse('submitdetail', kwargs={'pk': 1})
    #     print(33333333, url)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
