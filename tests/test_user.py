from . import BaseTestCase
import json


class TestUserRegistration(BaseTestCase):

    def setUp(self):
        """ Sets up the test client"""
        self.test_app = self.create_app().test_client()

    def test_user_registration(self):
        # successful user registration
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Successfully registered.'})

    def test_user_registration_of_an_already_existing_user(self):
        # register user
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Successfully registered.'})

        # re-register the user
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(message, {'Message': 'User could not be registered.'})

    def test_user_registration_with_incomplete_data(self):
        # missing password
        payload = dict(User="john")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Successfully registered.'})

        # missing username
        payload = dict(Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Successfully registered.'})


class TestUserLogin(BaseTestCase):
    def setUp(self):
        """ Sets up the test client"""
        self.test_app = self.create_app().test_client()

        # register the user to use in tests
        payload = dict(User="john", Password="password123")
        self.test_app.post('/api/v1/auth/register', data=payload)

    def test_user_login(self):
        # successful user login
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Successfully logged in.'})

    def test_user_login_with_incorrect_credentials(self):
        # with wrong password
        payload = dict(User="john", Password="wrongpass")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Login Failed.'})

        # with non-existent username
        payload = dict(User="nonexistent", Password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        to_pass = str(response.data, encoding='utf-8')
        message = json.loads(to_pass)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, {'Message': 'Login Failed.'})
