from . import BaseTestCase
import json


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
        self.assertIn(message, 'john')

    def test_user_registration_of_an_already_existing_user(self):
        # register user
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 409)
        self.assertIn(message, 'john')

        # re-register the user
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 409)
        self.assertIn(message, 'User could not be registered')

    def test_user_registration_with_incomplete_data(self):
        # missing password
        payload = dict(User="john")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, 'Successfully registered.')

        # missing username
        payload = dict(Password="password123")
        response = self.test_app.post('/api/v1/auth/register', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, 'password not provided')


class TestUserLogin(BaseTestCase):
    def setUp(self):
        """ Sets up the test client"""
        super(TestUserLogin, self).setUp()

        # register the user to use in tests
        payload = dict(User="john", Password="password123")
        self.test_app.post('/api/v1/auth/register', data=payload)

    def test_user_login(self):
        # successful user login
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn(message, 'Successfully logged in')

    def test_user_login_with_incorrect_credentials(self):
        # with wrong password
        payload = dict(User="john", Password="wrongpass")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertIn(message, 'Login Failed.')

        # with non-existent username
        payload = dict(User="nonexistent", Password="password123")
        response = self.test_app.post('/api/v1/auth/login', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message, 'Login Failed')

    def test_getting_an_authentication_token(self):
        payload = dict(User="john", Password="password123")
        response = self.test_app.post('/api/v1/auth/token', data=payload)
        message = str(response.data, encoding='utf-8')
        self.assertEqual(response.status_code, 200)
        assertIn(message, "Authorization")
