from django.test import TestCase
from ..models import Kitten


class KittenTest(TestCase):
    """ Test module for Kitten model """

    def setUp(self):
        Kitten.objects.create(
            name='Casper', age=3, breed='Cool Cat', color='Black')
        Kitten.objects.create(
            name='Muffin', age=1, breed='Uncool Cat', color='Brown')

    def test_puppy_breed(self):
        puppy_casper = Kitten.objects.get(name='Casper')
        puppy_muffin = Kitten.objects.get(name='Muffin')
        self.assertEqual(
            puppy_casper.get_breed(), 'Cool Cat')
        self.assertEqual(
            puppy_muffin.get_breed(), 'Uncool Cat')
