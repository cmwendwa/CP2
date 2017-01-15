from . import BaseTestCase
import json
from base64 import b64encode


class BucketlistsRouteTest(BaseTestCase):

    def setUp(self):
        """ Sets up the test client"""

        super(BucketlistsRouteTest, self).setUp()
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

    def test_creating_a_new_bucketlist(self):
        # successfully create a buckelist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        self.assertEqual(response.status_code, 201)

        received_data = str(response.data, encoding='utf-8')
        self.assertIn("name", received_data)
        self.assertIn("Cook", received_data)
        self.assertIn("items", received_data)
        self.assertIn("date_modified", received_data)
        self.assertIn("created_by", received_data)

        # create with missing name
        payload = {'notname': ""}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        self.assertEqual(response.status_code, 400)

        received_data = str(response.data, encoding='utf-8')
        self.assertIn("name not provided", received_data)

        # create an existing bucketlist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        self.assertEqual(response.status_code, 409)

        received_data = str(response.data, encoding='utf-8')
        self.assertIn("already exists", received_data)

    def test_retrieving_all_bucketlists(self):

        response = self.test_app.get(
            'api/v1/bucketlists/', headers=self.header)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("id", received_data)

    def test_retrieving_a_bucketlist(self):
        # add firsr bucketlist
        payload = {'name': "Cook"}
        print(payload)
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

        # retrieve first bucket list
        response = self.test_app.get(
            '/api/v1/bucketlists/1', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("Cook", received_data)
        # add a second bucketlist
        payload = {'name': "Play"}
        print(payload)
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # retrieve second bucketlist
        response = self.test_app.get(
            '/api/v1/bucketlists/2', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("Play", received_data)

        # retrieving a non existent item
        response = self.test_app.get(
            '/api/v1/bucketlists/3', headers=self.header)
        self.assertEqual(response.status_code, 404)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("bucketlist not found", received_data)

    def test_editing_a_bucket_list(self):
        # add a bucketlist
        payload = {'name': 'cook'}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # edit the addded bucketlist
        update = {'name': 'Cooking'}
        put_response = self.test_app.put(
            '/api/v1/bucketlists/1', data=update, headers=self.header)
        self.assertEqual(put_response.status_code, 200)
        received_data = str(put_response.data, encoding='utf-8')
        self.assertFalse('cook ' in received_data)
        self.assertIn('Cooking', received_data)
        self.assertIn('id', received_data)
        self.assertIn('date_created', received_data)

        # editing with a missing name
        put_response = self.test_app.put(
            '/api/v1/bucketlists/1', headers=self.header)
        self.assertEqual(put_response.status_code, 400)
        received_data = str(put_response.data, encoding='utf-8')
        self.assertFalse('New name not provided ' in received_data)

    def test_deleting_a_bucketlist(self):
        # add a bucketlist
        payload = {'name': 'cook'}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

        # delete bucketlist
        response = self.test_app.delete(
            '/api/v1/bucketlists/1', headers=self.header)
        received_data = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", received_data)

        # delete a non-existent item
        response = self.test_app.delete(
            '/api/v1/bucketlists/1', headers=self.header)
        received_data = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", received_data)
