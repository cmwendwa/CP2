from . import ApiBaseTest
import json


class BucketlistsRouteTest(ApiBaseTest):

    def setUp(self):
        """ Sets up the test client"""

        super(BucketlistsRouteTest, self).setUp()

    def test_creating_a_new_bucketlist(self):
        # successfully create a buckelist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        self.assertEqual(response.status_code, 201)

        received_data = str(response.data, encoding='utf-8')
        self.assertIn("name", received_data)
        self.assertIn("cook", received_data)
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
        # add six bucketlists
        # first
        payload = {'name': "cook"}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # second
        payload = {'name': 'plot'}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # third
        payload = {'name': "play"}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # fourth
        payload = {'name': "swim"}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # fifth
        payload = {'name': 'chase'}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # sixth
        payload = {'name': "travel"}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # seventh
        payload = {'name': "read"}
        self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

        # retrieve all bucketlists
        response = self.test_app.get(
            'api/v1/bucketlists/', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("cook", received_data)
        self.assertIn("plot", received_data)
        self.assertIn("swim", received_data)
        self.assertIn('"has_next": true', received_data)
        self.assertIn(
            "http://localhost/api/v1/bucketlists?limit=5&page=2", received_data)

        response = self.test_app.get(
            "api/v1/bucketlists/?limit=5&page=2", headers=self.header)
        #self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("read", received_data)
        self.assertIn("travel", received_data)

        # retrieving a single bucketlist using search
        response = self.test_app.get(
            'api/v1/bucketlists/?q=cook', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("id", received_data)
        self.assertIn("cook", received_data)
        self.assertIn("date_created", received_data)
        self.assertIn("date_modified", received_data)

        # test retrieving an item that does not exist by name
        response = self.test_app.get(
            'api/v1/bucketlists/?q=notthere', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("not found", received_data)

    def test_retrieving_a_bucketlist(self):
        # add firsr bucketlist
        payload = {'name': "Cook"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

        # retrieve first bucket list
        response = self.test_app.get(
            '/api/v1/bucketlists/1', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("cook", received_data)
        # add a second bucketlist
        payload = {'name': "Play"}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)
        # retrieve second bucketlist
        response = self.test_app.get(
            '/api/v1/bucketlists/2', headers=self.header)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("play", received_data)

        # retrieving a non existent item
        response = self.test_app.get(
            '/api/v1/bucketlists/3', headers=self.header)
        self.assertEqual(response.status_code, 404)
        received_data = str(response.data, encoding='utf-8')
        self.assertIn("bucketlist not found", received_data)

    def test_editing_a_bucket_list(self):
        # add a bucketlist
        # add firsr bucketlist
        payload = {'name': "Cook"}
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

        # editing a bucket list that's not there
        update = {'name': 'Cooking'}
        put_response = self.test_app.put(
            '/api/v1/bucketlists/33', data=update, headers=self.header)
        self.assertEqual(put_response.status_code, 404)
        received_data = str(put_response.data, encoding='utf-8')
        self.assertFalse('does not exist ' in received_data)

    def test_deleting_a_bucketlist(self):
        # add a bucketlist
        payload = {'name': 'cook'}
        response = self.test_app.post(
            '/api/v1/bucketlists/', data=payload, headers=self.header)

        # delete bucketlist
        response = self.test_app.delete(
            '/api/v1/bucketlists/1', headers=self.header)
        self.assertEqual(response.status_code, 204)
        response = self.test_app.get(
            '/api/v1/bucketlists/1', headers=self.header)
        self.assertEqual(response.status_code, 404)

        # delete a non-existent item
        response = self.test_app.delete(
            '/api/v1/bucketlists/1', headers=self.header)
        received_data = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", received_data)
