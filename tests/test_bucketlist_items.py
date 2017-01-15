from tests import BaseTestCase
import json
from base64 import b64encode


class TestBucketlistItems(BaseTestCase):
    def setUp(self):
        """ Sets up the test client"""

        super(TestBucketlistItems, self).setUp()
        # register user
        payload = dict(username="clement", password="password123")
        self.test_app.post('/api/v1/auth/register', data=payload)
        payload = dict(username="clement", password="password123")
        response = self.test_app.post(
            '/api/v1/auth/login', data=payload)

        # login user
        login_response = json.loads(str(response.data, encoding='utf-8'))
        token = login_response['Authorization']
        self.header = {'Authorization': ' Basic ' + b64encode(
            bytes(token + ':', 'ascii')).decode('ascii')}

        # create a bucketlist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        print(response)

    def test_creating_an_item(self):
        # create an item
        payload = {'name': 'cook lunch',
                   'description': 'ugali omena for lunch'}
        response = self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", received_data)
        self.assertIn("cook lunch", received_data)
        self.assertIn("description", received_data)
        self.assertIn("ugali omena for lunch", received_data)
        self.assertIn("date_created", received_data)

        # create without a description
        payload = {'name': 'cook supper',
                   'nodescription': 'chapati stew'}
        response = self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", received_data)
        self.assertIn("cook supper", received_data)
        self.assertIn("description", received_data)
        self.assertFalse("chapati stew" in received_data)
        self.assertIn("date_created", received_data)
        self.assertIn("done", received_data)
        self.assertIn("false", received_data)

        # with a missing name /mispelled
        payload = {'noname': 'cook breakfast',
                   'nodescription': 'chapati stew'}
        response = self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertIn("name not provided", received_data)
        # totally missing name
        response = self.test_app.post(
            '/api/v1/bucketlists/1/items/', headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertIn("name not provided", received_data)

    def test_bucket_editing_an_item(self):
        # add an item
        payload = {'name': 'cook lunch',
                   'description': 'ugali omena for lunch'}
        self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)

        # edit item /name and done
        payload = {'name': 'cooking lunch', 'done': True}
        put_response = self.test_app.put(
            '/api/v1/bucketlists/1/items/1', data=payload, headers=self.header)
        received_data = str(put_response.data, 'utf-8')
        self.assertEqual(put_response.status_code, 200)
        self.assertIn("name", received_data)
        self.assertIn("cooking lunch", received_data)
        self.assertFalse("cook lunch" in received_data)
        self.assertIn("done", received_data)
        self.assertIn("true", received_data)

    def test_deleting_an_item_from_a_bucketlist(self):
        # add an item
        payload = {'name': 'cook lunch',
                   'description': 'ugali omena for lunch'}
        self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)
        # delete item successfully
        response = self.test_app.delete(
            '/api/v1/bucketlists/1/items/1', headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", received_data)

        # deleting an item that's not existent
        response = self.test_app.delete(
            '/api/v1/bucketlists/1/items/23', headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", received_data)
