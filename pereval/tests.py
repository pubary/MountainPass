from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from pereval.models import Added, Coords, Level, Users
from pereval.serializers import AddedSerializer
from pereval.test_json import DATA as data


class SubmitDataTest(APITestCase):
    def setUp(self):
        self.coords = Coords.objects.create(latitude='1.23', longitude='4.56', height='789')
        self.level = Level.objects.create(winter='1', summer='', autumn='2', spring='3')
        self.user = Users.objects.create(email='123@45.6', fam='qaz', name='wer', otc='red')
        self.add = Added.objects.create(coords=self.coords, level=self.level, user=self.user, beauty_title='fine',
                                        title='good', other_titles='nice', add_time='2021-12-21 12:21:12', connect="")
        self.serializer_data = AddedSerializer(self.add).data

    def test_post(self):
        url = reverse('submitdata')
        response = self.client.post(url, data, format='json')
        add = Added.objects.get(title=data['title'])
        self.assertEqual(add.beauty_title, data['beauty_title'])
        self.assertEqual(add.other_titles, data['other_titles'])
        self.assertEqual(add.connect, data['connect'])
        self.assertEqual(f"{type(add.add_time)}", f"<class 'datetime.datetime'>")
        self.assertEqual(add.add_time.strftime("%S"), data['add_time'].split(":")[-1])
        self.assertEqual(add.status, 'new')
        self.assertEqual(add.user.email, data['user']['email'])
        self.assertEqual(add.user.fam, data['user']['fam'])
        self.assertEqual(add.user.name, data['user']['name'])
        self.assertEqual(add.user.otc, data['user']['otc'])
        self.assertEqual(str(add.coords.latitude), data['coords']['latitude'])
        self.assertEqual(str(add.coords.longitude), data['coords']['longitude'])
        self.assertEqual(str(add.coords.height), data['coords']['height'])
        self.assertEqual(add.level.winter, data['level']['winter'])
        self.assertEqual(add.level.summer, data['level']['summer'])
        self.assertEqual(add.level.autumn, data['level']['autumn'])
        self.assertEqual(add.level.spring, data['level']['spring'])
        self.assertEqual(response.data, {'status': 200, 'message': None, 'id': add.id})

    def test_invalid_get(self):
        url = reverse('submitdata')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 400, 'message': 'Not <email> in Request'})
    #
    def test_get_detail(self):
        url = reverse('submitdetail', kwargs={'pk': self.add.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.serializer_data.pop('send_time'), response.data.pop('send_time'))

    def test_get_email(self):
        url = reverse('submitdata')
        response = self.client.get(url + f'?user__email={self.add.user.email}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('id'), self.serializer_data.get('id'))
        self.assertEqual(response.data[0].get('title'), self.serializer_data.get('title'))

    def test_patch(self):
        url = reverse('submitdetail', kwargs={'pk': self.add.id})
        response = self.client.patch(url, data, format='json')
        add = Added.objects.get(title=data['title'])
        self.assertEqual(response.data, {'state': 1, 'message': 'Successfully'})
        self.assertEqual(add.beauty_title, data['beauty_title'])
        self.assertEqual(add.other_titles, data['other_titles'])

    def test_invalid_patch(self):
        pk = self.add.id + 1
        url = reverse('submitdetail', kwargs={'pk': pk})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.data, {'state': 0, 'message': 'Object does not exists'})

    def test_forbidden_patch(self):
        self.add.status = 'pending'
        self.add.save()
        url = reverse('submitdetail', kwargs={'pk': self.add.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.data, {'state': 0, 'message': 'Forbidden to edit'})



