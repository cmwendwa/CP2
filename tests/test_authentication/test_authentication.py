from tests import BaseTestCase
import json
from base64 import b64encode


class TestUserRegistration(BaseTestCase):

    def setUp(self):
        """ Sets up the test client"""
        super(TestUserRegistration, self).setUp()

    def test_user_registration(self):
        # successful user registration
        payload = dict(username="john", password="password123")
        response = self.test_app.post(
            '/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 201)
        self.assertIn('successfully added', message)

    def test_user_registration_of_an_already_existing_user(self):
        # register user
        payload = dict(username="john", password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 201)
        self.assertIn('successfully added', message)

        # re-register the user
        payload = dict(username="john", password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 409)
        self.assertIn('already exists', message)

    def test_user_registration_with_incomplete_data(self):
        # missing password
        payload = dict(username="john")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password not provided', message)

        # missing username
        payload = dict(Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertIn('username not provided', message)


class TestUserLogin(BaseTestCase):

    def setUp(self):
        """ Sets up the test client"""
        super(TestUserLogin, self).setUp()

        # register the user to use in tests
        payload = dict(username="john", password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        print(response.data)

    def test_user_login(self):
        # successful user login
        payload = dict(username="john", password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Authorization', message)

    def test_user_login_with_incorrect_credentials(self):
        # with wrong password
        payload = dict(username="john", password="wrongpass")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid password', message)

        # with non-existent username
        payload = dict(username="nonexistent", password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 403)
        self.assertIn(' username not found', message)

    # def test_getting_an_authentication_token(self):

    #     username = "john"
    #     password = "password123"
    #     header = {'Authorization': 'Bearer ' + b64encode(bytes(
    #               (username + ":" + password), 'ascii')).decode('ascii')}
    #     response = self.test_app.get('/api/v1/auth/token', headers=header)
    #     message = str(response.data, encoding='utf-8')
    #     #self.assertEqual(response.status_code, 200)
    #     self.assertIn("token", message)

    def test_accessing_index_resource_with_a_token(self):
        # with authentication
        payload = dict(username="john", password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        received_data = str(response.data, 'utf-8')
        token = json.loads(received_data)['Authorization']
        print("Token: ", str(token))
        header = {'Authorization': 'Token ' + token}

        response = self.test_app.get('api/v1/', headers=header)
        received_data = str(response.data, 'utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Bucketlist API', received_data)

        # without authentication
        response = self.test_app.get('api/v1/')
        self.assertEqual(response.status_code, 401)
        received_data = str(response.data, 'utf-8')
        self.assertIn('Unauthorized', received_data)
