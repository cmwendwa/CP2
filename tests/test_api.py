from . import BaseTestCase
import json


class BucketlistsRouteTest(BaseTestCase):

    def setUp(self):
        """ Sets up the test client"""
        self.test_app = self.create_app().test_client()

        payload = dict(User="john", Password="password123")
        self.test_app.post('/api/v1/auth/register', data=payload)

    def test_bucketlists_api_route_get(self):
        response = self.test_app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data,encoding='utf-8')
        self.assertIn("id:1", received_data)

    def test_bucketlists_api_route_get_missing_item(self):
        #deleted

        #non_existent

        pass

    def test_bucketlists_api_route_post(self):
        payload = dict(name="Cook lunch",
                       items=[],
                       )
        response = self.test_app.post('/api/v1/bucketlists/',data=payload)
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data,encoding='utf-8')
        self.assertIn("List succesfully added", received_data)
    def test_bucketlists_api_route_post_not_executing_successfully(self):
        # missing name

        #already_exists



class BucketlistRouteTest(BaseTestCase):

    def test_bucketlist_api_route_get(self):
        response = self.test_app.get('/api/v1/bucketlists/3')
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data,encoding='utf-8')
        self.assertIn("Cook", received_data)

        response = self.test_app.get('/api/v1/bucketlists/2')
        self.assertEqual(response.status_code, 200)
        received_data = str(response.data,encoding='utf-8')
        self.assertIn(len(response.data), received_data)

    def test_bucketlist_api_route_post(self):
        response = self.test_app.post('/api/v1/bucketlists/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)

    def test_bucketlist_api_route_put(self):
        response = self.test_app.get('/api/v1/bucketlists/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)

    def test_bucketlist_api_route_delete(self):
        response = self.test_app.delete('/api/v1/bucketlists/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)



class BucketItemRouteTest(BaseTestCase):
    def test_bucket_item_api_route_get(self):
        response = self.test_app.get('/api/v1/bucketlists/3/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)

    def test_bucket_item_api_route_post(self):
        response = self.test_app.get('/api/v1/bucketlists/3/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)

    def test_bucket_item_api_route_put(self):
        response = self.test_app.get('/api/v1/bucketlists/3/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)

    def test_bucket_item_api_route_delete(self):
        response = self.test_app.get('/api/v1/bucketlists/3/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 21)


class AdditionalFunctionalityTest(BaseTestCase):

    def test_pagination(self):
        # given limit possible

        #given limit greater than available 


        pass

    def test_searching_by_name(self):
        #search an existent item

        #search a non-existent item
        pass
