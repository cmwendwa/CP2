from flask_testing import TestCase
from app import app, db
from config import config


class BaseTestCase(TestCase):
    def create_app(self):
        """"Sets up the testing app"""

        # configuring the app to use testing settings
        app.config.from_object(config['testing'])
        db.create_all()


        return app

    def setUp(self):
        """Adds resources for use int the test suites"""
        # Sets up the test client"""
        self.test_app = self.create_app().test_client()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
