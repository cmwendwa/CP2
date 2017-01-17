import json
from . import ApiBaseTest


class TestBucketlistItems(ApiBaseTest):
    def setUp(self):
        """ Sets up the test client"""

        super(TestBucketlistItems, self).setUp()

        # create a bucketlist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

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

        # create an existing item
        payload = {'name': 'cook lunch',
                   'description': 'ugali omena for lunch'}
        response = self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 409)
        self.assertIn("already exists", received_data)

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

        # creating an item in a bucketlist that doesn't exist
        payload = {'name': 'swim',
                   'description': 'go for swimming at ymca'}
        response = self.test_app.post(
            '/api/v1/bucketlists/13/items/', data=payload, headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", received_data)

    def test_bucket_editing_an_item(self):
        # add an item
        payload = {'name': 'cook lunch',
                   'description': 'ugali omena for lunch'}
        self.test_app.post(
            '/api/v1/bucketlists/1/items/', data=payload, headers=self.header)

        # edit item /name and done
        payload = {'name': 'cooking lunch',
                   'description': 'cooking ugali stew for lunch', 'done': True}
        put_response = self.test_app.put(
            '/api/v1/bucketlists/1/items/1', data=payload, headers=self.header)
        received_data = str(put_response.data, 'utf-8')
        self.assertEqual(put_response.status_code, 200)
        self.assertIn("name", received_data)
        self.assertIn("cooking lunch", received_data)
        self.assertFalse("cook lunch" in received_data)
        self.assertIn("done", received_data)
        self.assertIn("true", received_data)
        self.assertIn("cooking ugali stew for lunch", received_data)

        # edit an item that does not exist
        payload = {'name': 'cooking lunch', 'done': True}
        put_response = self.test_app.put(
            '/api/v1/bucketlists/1/items/13', data=payload, headers=self.header)
        received_data = str(put_response.data, 'utf-8')
        self.assertEqual(put_response.status_code, 404)
        self.assertIn("does not exist", received_data)

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
