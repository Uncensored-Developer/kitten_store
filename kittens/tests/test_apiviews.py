import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Kitten
from ..serializers import KittenSerializer


# initialize the APIClient app
client = Client()


class GetAllKittensTest(TestCase):
    """ Test module for GET all kittens API """

    def setUp(self):
        Kitten.objects.create(
            name='Casper', age=3, breed='Cool Cat', color='Black')
        Kitten.objects.create(
            name='Muffin', age=1, breed='Uncool Cat', color='Brown')
        Kitten.objects.create(
            name='Rambo', age=2, breed='Angry Cat', color='Black')
        Kitten.objects.create(
            name='Ricky', age=6, breed='Calm Cat', color='Brown')

    def test_get_all_kittens(self):
        # get API response
        response = client.get(reverse('get_post_kittens'))
        # get data from db
        puppies = Kitten.objects.all()
        serializer = KittenSerializer(puppies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleKittenTest(TestCase):
    """ Test module for GET single kitten API """

    def setUp(self):
        self.casper = Kitten.objects.create(
            name='Casper', age=3, breed='Cool Cat', color='Black')
        self.muffin = Kitten.objects.create(
            name='Muffin', age=1, breed='Uncool Cat', color='Brown')
        self.rambo = Kitten.objects.create(
            name='Rambo', age=2, breed='Angry Cat', color='Black')
        self.ricky = Kitten.objects.create(
            name='Ricky', age=6, breed='Calm Cat', color='Brown')

    def test_get_valid_single_kitten(self):
        response = client.get(
            reverse('get_delete_update_kitten', kwargs={'pk': self.rambo.pk}))
        kitten = Kitten.objects.get(pk=self.rambo.pk)
        serializer = KittenSerializer(kitten)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_kitten(self):
        response = client.get(
            reverse('get_delete_update_kitten', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewKittenTest(TestCase):
    """ Test module for inserting a new kitten """

    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'age': 4,
            'breed': 'Cool Cat',
            'color': 'White'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Uncool Cat',
            'color': 'White'
        }

    def test_create_valid_kitten(self):
        response = client.post(
            reverse('get_post_kittens'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_kitten(self):
        response = client.post(
            reverse('get_post_kittens'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleKittenTest(TestCase):
    """ Test module for updating an existing kitten record """

    def setUp(self):
        self.casper = Kitten.objects.create(
            name='Casper', age=3, breed='Cool Cat', color='Black')
        self.muffin = Kitten.objects.create(
            name='Muffy', age=1, breed='Uncool Cat', color='Brown')
        self.valid_payload = {
            'name': 'Muffy',
            'age': 2,
            'breed': 'Angry Cat',
            'color': 'Black'
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Calm Cat',
            'color': 'White'
        }

    def test_valid_update_kitten(self):
        response = client.put(
            reverse('get_delete_update_kitten', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_kitten(self):
        response = client.put(
            reverse('get_delete_update_kitten', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleKittenTest(TestCase):
    """ Test module for deleting an existing kitten record """

    def setUp(self):
        self.casper = Kitten.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Kitten.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')

    def test_valid_delete_kitten(self):
        response = client.delete(
            reverse('get_delete_update_kitten', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_kitten(self):
        response = client.delete(
            reverse('get_delete_update_kitten', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
