import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Puppy
from ..serializers import PuppySerializer

# initialize the APIClient app
client = Client()


class GetAllPuppiesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Puppy.objects.create(name='Casper',
                             age=3,
                             breed='Bull Dog',
                             color='Black')
        Puppy.objects.create(name='Muffin',
                             age=1,
                             breed='Gradane',
                             color='Brown')
        Puppy.objects.create(name='Rambo',
                             age=2,
                             breed='Labrador',
                             color='Black')
        Puppy.objects.create(name='Ricky',
                             age=6,
                             breed='Labrador',
                             color='Brown')

    # 测试GET所有
    def test_get_all_puppies(self):
        # get API response
        # reverse（定义的urls.py的name)可以获取到完整的url
        response = client.get(reverse('get_post_puppies'))
        # get data from db
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 测试GET单个，不存在的情况
    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# 测试POST，分别测试茶创建成功和失败的情况
class CreateNewPuppyTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_create_valid_puppy(self):
        response = client.post(reverse('get_post_puppies'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_puppy(self):
        response = client.post(reverse('get_post_puppies'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# 验证更新成功和失败
class UpdateSinglePuppyTest(TestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        self.casper = Puppy.objects.create(name='Casper',
                                           age=3,
                                           breed='Bull Dog',
                                           color='Black')
        self.muffin = Puppy.objects.create(name='Muffy',
                                           age=1,
                                           breed='Gradane',
                                           color='Brown')
        self.valid_payload = {
            'name': 'Muffy',
            'age': 2,
            'breed': 'Labrador',
            'color': 'Black'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_valid_update_puppy(self):
        response = client.put(reverse('get_delete_update_puppy',
                                      kwargs={'pk': self.muffin.pk}),
                              data=json.dumps(self.valid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_puppy(self):
        response = client.put(reverse('get_delete_update_puppy',
                                      kwargs={'pk': self.muffin.pk}),
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# 验证删除成功和失败的情况
class DeleteSinglePuppyTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.casper = Puppy.objects.create(name='Casper',
                                           age=3,
                                           breed='Bull Dog',
                                           color='Black')
        self.muffin = Puppy.objects.create(name='Muffy',
                                           age=1,
                                           breed='Gradane',
                                           color='Brown')

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)