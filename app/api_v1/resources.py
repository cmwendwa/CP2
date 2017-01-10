from flask import Flask, g
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy


class RegisterApi(Resource):
    def post(self):

        return {'message': 'None'}


class LoginApi(Resource):
    def post(self):

        return {'message': 'None'}

class GetToken(Resource):
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}


class BucketlistsApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='Buckestlist  name not provided', location='json')

        super(BucketlistsApi, self).__init__()

    def post(self):
        return {"SHit": True}

    def get(self):
        pass
        # return {"SHit": True}


class BucketlistApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('list_id', type=str, required=True,
                                   help='Bucket list id not provided',
                                   location='json')
        super(BucketlistApi, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class BucketItemsApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=str, required=True,
                                   help='Bucket list id not provided',
                                   location='json')
        self.reqparse.add_argument('item_id', type=str, required=True,
                                   help='Item id not provided',
                                   location='json')
        super(BucketItemsApi, self).__init__()

    def post(self):
        pass

    def put(self, id, item_id):
        pass

    def delete(self, id, item_id):
        pass

    def get(self, id, item_id):
        pass


class Search(Resource):
    def get(self):
        pass
