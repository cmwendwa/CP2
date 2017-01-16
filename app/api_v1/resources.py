from flask import abort, request, jsonify, url_for, g
from ..models import User, Bucketlist, Item
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from app import db
from ..serializers import bucketlist_serializer, item_serializer

auth = HTTPBasicAuth()

from base64 import b32encode


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class RegisterApi(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'username', type=str, required=True, help='username not provided', location='form')
        self.parse.add_argument(
            'password', type=str, required=True, help='password not provided', location='form')
        super(RegisterApi, self).__init__()

    def post(self):
        args = self.parse.parse_args()
        username = args['username']
        password = args['password']
        if User.query.filter_by(username=username).first() is not None:
            return {'message': "User already exists"}, 409  # existing user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User successfully added'}, 201


class LoginApi(Resource):
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.parse.add_argument(
            'username', type=str, required=True, help='username not provided', location='form')
        self.parse.add_argument(
            'password', type=str, required=True, help='password not provided', location='form')
        super(LoginApi, self).__init__()

    def post(self):
        args = self.parse.parse_args()
        username = args['username']
        password = args['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if user.verify_password(password):
                token = user.generate_auth_token()
                return {'Authorization': token.decode('ascii')}
            else:
                return {'message': 'Invalid password'}, 400

        else:
            return {'message': 'Invalid username'}, 400


class GetTokenApi(Resource):
    @auth.login_required
    def get(self):
        """
        This is the token endpoint and returns the authentication token of a logged a user
        tags:
          - Bucketlist API
        parameters:
          -
        responses:
          500:
            description: Server error!
          200:
            description: successful request
            schema:
          404:
            description: Not logged in.
          400:
            description: Error logging in


        """
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}, 200


class IndexResource(Resource):
    @auth.login_required
    def get(self):
        """
        This is the bucketlist API
        Call this api to create a Bucketlists of things you want to do, add items to this 
        bucketlist, view, edit and delete bucketlists and items 
        ---
        tags:
          - Bucketlist API
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

        return {'message': "Welcome to Bucketlist API"}


class BucketlistsApi(Resource):
    @auth.login_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('name', type=str, required=True,
                           help='Buckestlist  name not provided', location='form')
        args = parse.parse_args()
        name = args['name']
        if Bucketlist.query.filter_by(name=name).first() == None:
            created_by = g.user.id
            new_bucketlist = Bucketlist(name, created_by)
            db.session.add(new_bucketlist)
            db.session.commit()
            new_bucketlist = new_bucketlist
            return marshal(new_bucketlist, bucketlist_serializer), 201
        else:
            return {'message': "Bucketlist already exists"}, 409

    @auth.login_required
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('page', type=int, location='json')
        parse.add_argument('limit', type=int, location='json')
        parse.add_argument('q', type=str, location='args')
        args = parse.parse_args()
        search_name = args['q']
        limit = args['limit']
        page_no = args['page']

        if search_name:
            search_results = Bucketlist.query.filter_by(
                name=name, created_by=g.user.id).paginate(page, limit, False)

            if search_results:
                return marshal(search_results, bucketlist_serializer)
            else:
                return {'message': 'Bucketlist ' + search_name + ' not found.'}, 404
        all_bucketlists = Bucketlist.query.filter_by(
            created_by=g.user.id).first()
        return marshal(all_bucketlists, bucketlist_serializer)


class BucketlistApi(Resource):

    @auth.login_required
    def get(self, id):
        got_list = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if not got_list == None:
            return marshal(got_list, bucketlist_serializer)
        else:
            return {'message': 'Specified bucketlist not found.'}, 404

    @auth.login_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='New name not provided', location='form')
        args = parser.parse_args()
        new_name = args['name']

        got_list = Bucketlist.query.filter_by(
            id=id, created_by=g.user.id).first()
        if not got_list == None:
            got_list.name = new_name
            db.session.add(got_list)
            db.session.commit()
            return marshal(got_list, bucketlist_serializer)

        else:
            return {'message': 'Specified bucketlist not found.'}, 404

    @auth.login_required
    def delete(self, id):
        to_delete = Bucketlist.query.filter_by(
            created_by=g.user.id, id=id).first()
        if not to_delete == None:
            db.session.delete(to_delete)
            db.session.commit()
            return {'message': 'Bucketlist successfully deleted'}
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
        args = self.parse.parse_args()
        item_name = args['name']
        description = args['description']
        bucketlist_id = id
        bucketlist = Bucketlist.query.filter_by(
            id=bucketlist_id, created_by=g.user.id).first()
        if not bucketlist:
            return {'message': 'The bucketlist you want to insert an item to does not exists.'}

        if Item.query.filter_by(name=item_name, bucketlist_id=bucketlist_id).first():
            return {'message': 'An item with the provided item name already exists.'}, 409
        if description:
            new_item = Item(item_name, bucketlist_id, description)
        else:
            new_item = Item(item_name, bucketlist_id)
        db.session.add(new_item)
        db.session.commit()
        created_item = new_item

        return marshal(new_item, item_serializer)


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
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('done', type=bool)
        parser.add_argument('description', type=bool)
        edit_item = Item.query.filter_by(bucketlist_id=id, id=item_id).first()

        if edit_item == None:
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
                edit_item.name = name
            db.session.add(edit_item)
            db.session.commit()
            return marshal(edit_item, item_serializer)

    @auth.login_required
    def delete(self, id, item_id):

        delete_item = Item.query.filter_by(
            bucketlist_id=id, id=item_id).first()
        if delete_item == None:
            return {'message': 'The item you tried to delete does not exist.'}, 404
        db.session.delete(delete_item)
        db.session.commit()

        return {'message': 'Item was successfully deleted'}, 200
