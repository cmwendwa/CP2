from flask import abort, request, jsonify, url_for, g
from ..models import User, Bucketlist, Item
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from app import db
from ..serializers import bucketlist_serializer, item_serializer
from base64 import b32encode
from sqlalchemy import exc
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """verifies token"""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class RegisterApi(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'username',
            type=str,
            required=True,
            help='username not provided',
            location='form')
        self.parse.add_argument(
            'password',
            type=str,
            required=True,
            help='password not provided',
            location='form')
        super(RegisterApi, self).__init__()

    def post(self):
        """
        Register a new user given a username and a password

        parameters:
          -username
          -password

        """
        args = self.parse.parse_args()
        username = args['username']
        password = args['password']
        try:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'User successfully added'}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': "User already exists"}, 409


class LoginApi(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'username',
            type=str,
            required=True,
            help='username not provided',
            location='form')
        self.parse.add_argument(
            'password',
            type=str,
            required=True,
            help='password not provided',
            location='form')
        super(LoginApi, self).__init__()

    def post(self):
        """
        Logs in the user given a username and a password and return an authentication token for a
        successful login

        parameters:
          -username
          -password

        """

        args = self.parse.parse_args()
        username = args['username'].lower()
        password = args['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_auth_token()
                return {'Authorization': token.decode('ascii')}
            if not user.verify_password(password):
                return {'message': 'Invalid password '}, 403
        else:
            return {'message': 'Specified username not found '}, 403


class IndexResource(Resource):

    @auth.login_required
    def get(self):
        """
        This is the bucketlist API
        Call this api to create a Bucketlists of things you want to do, add items to this
        bucketlist, view, edit and delete bucketlists and items
        ---
        parameters:
          -
        responses:
          500:
            description: Server error!
          200:
            description: user token
            schema:
              token
          404:
            description: Not logged in.logged in
          400:
            description: Error logging in

        """

        return {'message': "Welcome to Bucketlist API"}, 200


class BucketlistsApi(Resource):

    @auth.login_required
    def post(self):
        """
        Creates a new bucketlst given the name

        parameters:
          -name
        """

        parse = reqparse.RequestParser()
        parse.add_argument(
            'name',
            type=str,
            required=True,
            help='Buckestlist  name not provided',
            location='form')
        args = parse.parse_args()
        name = args['name'].casefold()
        if Bucketlist.query.filter_by(
                name=name, created_by=g.user.id).first() is None:
            created_by = g.user.id
            new_bucketlist = Bucketlist(name, created_by)
            db.session.add(new_bucketlist)
            db.session.commit()
            new_bucketlist = new_bucketlist
            return {"successfully created: ": marshal(
                new_bucketlist, bucketlist_serializer)}, 201
        else:
            return {'message': "Bucketlist already exists"}, 409

    @auth.login_required
    def get(self):
        """
        Returns bucketlists created by a given user, the returned lists are paginated. The 'q' argument
        is used to search a bucketlist by name.

        parameters:
          -limit
          -page
          -id
          -q
       """
        parse = reqparse.RequestParser()
        parse.add_argument('page', type=int, default=1)
        parse.add_argument('limit', type=int, default=5)
        parse.add_argument('q', type=str, location='args')
        args = parse.parse_args()
        search_name = args['q']
        limit = args['limit']
        page_no = args['page']
        # implement search function/option
        if search_name:
            search_results = Bucketlist.query.filter_by(
                name=search_name.casefold(), created_by=g.user.id).first()

            if search_results:
                return {
                    "Found ": marshal(
                        search_results,
                        bucketlist_serializer)}
            else:
                return {'message': 'Bucketlist ' + search_name + ' not found.'}
        # get all bucketlists and paginate
        bucketlists_per_page = Bucketlist.query.filter_by(
            created_by=g.user.id).paginate(
                page=page_no, per_page=limit, error_out=True)

        all_bucketlists = bucketlists_per_page.pages

        has_next = bucketlists_per_page.has_next
        has_previous = bucketlists_per_page.has_prev
        if has_next:
            next_page = str(request.url_root) + 'api/v1/bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page_no + 1)
        else:
            next_page = 'None'
        if has_previous:
            previous_page = request.url_root + 'api/v1/bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page_no - 1)
        else:
            previous_page = 'None'

        bucketlists = bucketlists_per_page.items

        response = {'bucketlists': marshal(bucketlists, bucketlist_serializer),
                    'has_next': has_next,
                    'pages': all_bucketlists,
                    'previous_page': previous_page,
                    'next_page': next_page
                    }
        return response


class BucketlistApi(Resource):

    @auth.login_required
    def get(self, id):
        """
        Returns the bucketlist with the given id

        parameters:
          -id

        """

        got_list = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if got_list:
            return marshal(got_list, bucketlist_serializer)
        else:
            return {'message': 'Specified bucketlist not found.'}, 404

    @auth.login_required
    def put(self, id):
        """
        Edits/updates the bucketlist with the given id

        parameters:
          -name
          -id
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='New name not provided', location='form')
        args = parser.parse_args()
        new_name = args['name']

        got_list = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if not got_list is None:
            got_list.name = new_name
            db.session.add(got_list)
            db.session.commit()
            return {"successfully edited ": marshal(
                got_list, bucketlist_serializer)}, 200

        else:
            return {'message': 'Specified bucketlist not found.'}, 404

    @auth.login_required
    def delete(self, id):
        """
        Deletes the bucketlist with the given id

        parameters:
          -id
        """
        to_delete = Bucketlist.query.filter_by(
            created_by=g.user.id, id=id).first()
        if not to_delete is None:
            db.session.delete(to_delete)
            db.session.commit()
            return {'message': 'Bucketlist successfully deleted'}, 204
        else:
            return {'message': 'Not deleted, Bucketlist does not exist'}, 404


class BucketlistItemCreateApi(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('name', type=str, required=True,
                                help='Item name not provided',
                                location='form')
        self.parse.add_argument('description', type=str,
                                location='form')

    @auth.login_required
    def post(self, id):
        """
        Creates a new item in the bucketlist with the provided id

        parameters:
          -name
          -description
          -id
          -item_id

        """
        args = self.parse.parse_args()
        item_name = args['name']
        description = args['description']
        bucketlist_id = id
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()
        if not bucketlist:
            return {
                'message': 'The bucketlist you want to insert an item to does not exists.'}, 404

        if Item.query.filter_by(
                name=item_name,
                bucketlist_id=bucketlist_id).first():
            return {
                'message': 'An item with the provided item name already exists.'}, 409
        if description:
            new_item = Item(item_name, bucketlist_id, description)
        else:
            new_item = Item(item_name, bucketlist_id)
        db.session.add(new_item)
        db.session.commit()
        created_item = new_item

        return {"successfuly created: ": marshal(new_item, item_serializer)}, 201


class BucketItemsApi(Resource):

    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('name', type=str, required=True,
                                help='Bucket list id not provided',
                                location='form')
        self.parse.add_argument('description', type=str,
                                location='form')
        super(BucketItemsApi, self).__init__()

    @auth.login_required
    def put(self, id, item_id):
        """
        Edits/updates the an item with the given item_id and within the bucketlist with the given id

        parameters:
          -name
          -description
          -done
          -id
          -item_id


        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('done', type=bool)
        parser.add_argument('description', type=str)
        edit_item = Item.query.filter_by(bucketlist_id=id, id=item_id).first()

        if edit_item is None:
            return {'message': 'The item you tried to edit does not exist.'}, 404
        else:
            args = parser.parse_args()
            done = args['done']
            name = args['name']
            description = args['description']
            if done:
                edit_item.done = done
            if name:
                edit_item.name = name
            if description:
                edit_item.description = description
            db.session.add(edit_item)
            db.session.commit()
            return {
                "successfully upadated: ": marshal(
                    edit_item, item_serializer)}, 200

    @auth.login_required
    def delete(self, id, item_id):
        """
        Deletes the an item with the given item_id and within the bucketlist with the given id

        parameters:
          -id
          -item_id

        """

        delete_item = Item.query.filter_by(
            bucketlist_id=id, id=item_id).first()
        if delete_item is None:
            return {
                'message': 'The item you tried to delete does not exist.'}, 404
        db.session.delete(delete_item)
        db.session.commit()

        return {'message': ''}, 204
