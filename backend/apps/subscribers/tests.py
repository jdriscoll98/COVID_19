from django.test import TestCase
from apps.subscribers.models import Subscriber
from apps.subscribers.serializers import SubscriberSerializer
from django.test import Client

class SubscriberModelTestCase(TestCase):
    def setUp(self):
        Subscriber.objects.create(telephone='+19548091951', location='cooper city')
        client = Client()

    def test_string(self):
        subscriber = Subscriber.objects.get(telephone='+19548091951')
        ## Upon initialization, subscribers are not verified
        self.assertEqual("+19548091951 | False", str(subscriber))

class SubscriberSerializerTest(TestCase):
    def setUp(self):
        Subscriber.objects.create(
            telephone='+19548091951', location='cooper city')
        client = Client()

    def test_requires_phone_number(self):
        example_location = '{"locality": "Gainesville", "administrative_area_level_1": "FL", \
                            "country": "United States", "latitude": 29.6516344, "longitude": -82.32482619999999}'

        response = self.client.post(
            '/api/subscribers/', {'telephone': '', 'location': example_location})
        error = response.json()['telephone'][0]

        self.assertEqual('This field may not be blank.', error)

    def test_invalid_phone_number(self):
        example_location = '{"locality": "Gainesville", "administrative_area_level_1": "FL", \
                    "country": "United States", "latitude": 29.6516344, "longitude": -82.32482619999999}'

        response = self.client.post(
            '/api/subscribers/', {'telephone': '1', 'location': example_location})
        error = response.json()['telephone'][0]

        self.assertEqual('Please enter a valid phone number', error)
        

    def test_unverfied_reregisration(self):
        example_location = '{"locality": "Gainesville", "administrative_area_level_1": "FL", \
                    "country": "United States", "latitude": 29.6516344, "longitude": -82.32482619999999}'

        response = self.client.post(
            '/api/subscribers/', {'telephone': '(954) 809-1951', 'location': example_location})

        self.assertEqual(response.status_code, 201)

    def test_number_already_verified(self):
        example_location = '{"locality": "Gainesville", "administrative_area_level_1": "FL", \
                    "country": "United States", "latitude": 29.6516344, "longitude": -82.32482619999999}'
        
        subscriber = Subscriber.objects.get(telephone='+19548091951')
        subscriber.verified = True
        subscriber.save()

        response = self.client.post(
            '/api/subscribers/', {'telephone': '(954) 809-1951', 'location': example_location})

        error = response.json()['telephone'][0]
        self.assertEqual("Sorry, this number is already registered", error)

    def test_invalid_location(self):
        response = self.client.post(
            '/api/subscribers/', {'telephone': '(954) 809-1952', 'location': '{}'})

        error = response.json()['location'][0]
        self.assertEqual("Please use the autocomplete feature for the location", error)

class SubscriberViewTest(TestCase):
    def setUp(self):
        client = Client()
        
    def test_list_response(self):
        response = self.client.get('/api/subscribers')
        self.assertEqual({}, response.json)
