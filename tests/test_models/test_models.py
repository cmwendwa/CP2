from app.models import Bucketlist, Item, User
from datetime import datetime
from tests import BaseTestCase, db
from time import sleep


class TestModels(BaseTestCase):
    def setUp(self):
        super(TestModels, self).setUp()
        bucketlist = Bucketlist("Cook")
        db.session.add(bucketlist)
        db.session.commit()
        self.reload_list = bucketlist

    def test_creating_bucketlist(self):
        """Tests successfully creating a bucketlist"""

        # this test would conflict with bucketlist defined in the setup
        # clear everythin before running it
        db.drop_all()
        db.create_all()

        # Instantiating a bucketlist object
        bucketlist = Bucketlist("Cook")
        # save the object to database
        db.session.add(bucketlist)
        db.session.commit()

        # load the saved object
        reload_list = bucketlist

        # asssert the attributes
        self.assertEqual(reload_list.id, 1)
        self.assertEqual(reload_list.name, "Cook")
        self.assertEqual(reload_list.created_by, None)
        year = str(datetime.today().year)
        self.assertIn(year, str(reload_list.date_created))
        self.assertIn(year, str(reload_list.date_modified))
        self.assertEqual(len(reload_list.items), 0)

        # create another bucket object, save it to db and asser its attributes
        bucketlist = Bucketlist("Play")
        db.session.add(bucketlist)
        db.session.commit()
        reload_list = bucketlist
        self.assertEqual(reload_list.id, 2)
        self.assertEqual(reload_list.name, "Play")
        self.assertEqual(reload_list.created_by, None)
        year = str(datetime.today().year)
        self.assertIn(year, str(reload_list.date_created))
        self.assertIn(year, str(reload_list.date_modified))
        self.assertEqual(len(reload_list.items), 0)
        # test querying bucketlists
        bucketlist_query = Bucketlist.query.all()
        self.assertIn("<Bucketlist 'Cook'>", str(bucketlist_query))
        self.assertIn("<Bucketlist 'Play'>", str(bucketlist_query))
        self.assertFalse("<Bucketlist 'Not in'>" in str(bucketlist_query))

    def test_creating_bucketlist_with_a_missing_name(self):
        """Tests successfully creating a bucketlist"""

        # this test would conflict with bucketlist defined in the setup
        # clear everythin before running it
        db.drop_all()
        db.create_all()

        with self.assertRaises(Exception) as context:

            # Instantiating a bucketlist object
            bucketlist = Bucketlist()
            # save the object to database
            db.session.add(bucketlist)
            db.session.commit()

            self.assertTrue(
                ' __init__() missing 1 required positional argument' in context.exception)

    def test_editing_bucket_list(self):

        self.assertEqual(self.reload_list.id, 1)
        self.assertEqual(self.reload_list.name, "Cook")

        self.reload_list.name = "Cooking"
        db.session.add(self.reload_list)
        db.session.commit()
        re_reload_list = Bucketlist.query.get(1)
        self.assertEqual(re_reload_list.id, 1)
        self.assertEqual(re_reload_list.name, "Cooking")

    def test_deleting_bucketlist(self):

        self.assertEqual(self.reload_list.id, 1)
        self.assertEqual(self.reload_list.name, "Cook")

        db.session.delete(self.reload_list)
        db.session.commit()
        bucketlist = Bucketlist.query.get(1)
        # assert not found in database
        self.assertEqual(bucketlist, None)

    def test_creating_an_item(self):
        self.assertEqual(self.reload_list.id, 1)
        self.assertEqual(self.reload_list.name, "Cook")

        item = Item("Cook lunch", self.reload_list.id, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()

        reload_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()
        self.assertEqual(reload_item.name, "Cook lunch")
        self.assertEqual(reload_item.description, "Coooking Ugali omena")
        self.assertEqual(reload_item.done, False)
        year = str(datetime.today().year)
        self.assertIn(year, str(reload_item.date_created))
        self.assertIn(year, str(reload_item.date_modified))

        # test querying items
        item_query = Item.query.all()
        self.assertIn("<Item 'Cook lunch'>", str(item_query))
        self.assertFalse("<Item 'Not in'>" in str(item_query))

        # creating an item with a missing name results in an error

        with self.assertRaises(Exception) as context:

            # Instantiating a bucketlist object
            item = Item()
            # save the object to database
            db.session.add(item)
            db.session.commit()

            self.assertTrue(
                ' __init__() missing 1 required positional argument name' in context.exception)

    def test_editing_an_item(self):

        self.assertEqual(self.reload_list.id, 1)
        self.assertEqual(self.reload_list.name, "Cook")

        item = Item("Cook lunch", 1, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()

        reload_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(reload_item.name, "Cook lunch")
        self.assertEqual(reload_item.description, "Coooking Ugali omena")
        self.assertEqual(reload_item.done, False)

        reload_item.description = "Coooking Ugali fish"
        reload_item.done = True
        db.session.add(reload_item)
        db.session.commit()

        re_reload_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(re_reload_item.description, "Coooking Ugali fish")
        self.assertEqual(re_reload_item.done, True)

    def test_deleting_an_item(self):
        self.assertEqual(self.reload_list.id, 1)
        self.assertEqual(self.reload_list.name, "Cook")

        item = Item("Cook lunch", 1, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()
        reload_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()
        self.assertEqual(reload_item.name, "Cook lunch")
        self.assertEqual(reload_item.description, "Coooking Ugali omena")
        self.assertEqual(reload_item.done, False)
        # assert not found in database
        db.session.delete(reload_item)

        reload_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(reload_item, None)

    def test_creating_user(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()

        reload_user = user
        self.assertEqual(reload_user.id, 1)
        self.assertEqual(reload_user.username, "clement")

        # test querying users
        user_query = User.query.all()
        self.assertIn("<User 'clement'", str(user_query))

    def test_user_password_inaccessible(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()
        with self.assertRaises(Exception) as context:
            user.password
            self.assertTrue('not a readable' in context.exception)

    def test_expired_auth_token(self):
        user = User('Imani', 'imani123')
        token = user.generate_auth_token(0.5)
        sleep(1)
        verification = user.verify_auth_token(token)
        self.assertEqual(verification, None)

    def test_deleting_user(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()

        reload_user = user
        self.assertEqual(reload_user.id, 1)
        self.assertEqual(reload_user.username, "clement")

        db.session.delete(user)
        db.session.commit()

        re_reload_user = User.query.filter_by(id=1).first()
        # assert not found in database
        self.assertEqual(re_reload_user, None)

    def TearDown(self):
        super(TestModels, self).TearDown
