from flask_testing import TestCase
from manage import app
from config import config


class BaseTestCase(TestCase):
    def create_app(self):
        """"Sets up the testing app"""

        app.config.from_object(config['testing'])

        return app
