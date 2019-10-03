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

    def test_get_all_puppies(self):
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

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_kitten', kwargs={'pk': self.rambo.pk}))
        kitten = Kitten.objects.get(pk=self.rambo.pk)
        serializer = KittenSerializer(kitten)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_kitten', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
