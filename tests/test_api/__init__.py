from tests import BaseTestCase
from base64 import b64encode
import json


class ApiBaseTest(BaseTestCase):
    def setUp(self):
        super(ApiBaseTest, self).setUp()
        # register user
        payload = dict(username="clement", password="password123")
        self.test_app.post('/api/v1/auth/register', data=payload)
        payload = dict(username="clement", password="password123")
        response = self.test_app.post(
            '/api/v1/auth/login', data=payload)

        # login user
        login_response = json.loads(str(response.data, encoding='utf-8'))
        token = login_response['Authorization']
        self.header = {'Authorization': 'Token ' + token}


class TestApi(ApiBaseTest):
    def test_index_resource(self):
        # with authentication
        response = self.test_app.get('api/v1/', headers=self.header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucketlist API', received_data)

        # without authentication
        response = self.test_app.get('api/v1/')
        self.assertEqual(response.status_code, 401)
        received_data = str(response.data, 'utf-8')
        self.assertIn('Unauthorized', received_data)
