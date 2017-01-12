from flask_restful import Api
from app import app
from .resources import RegisterApi, LoginApi, BucketlistsApi, BucketlistApi, BucketItemsApi, GetTokenApi, BucketlistItemCreateApi


api = Api(app=app, prefix='/api/v1')


api.add_resource(RegisterApi, '/auth/register', endpoint='register')
api.add_resource(LoginApi, '/auth/login', endpoint='login')
api.add_resource(GetTokenApi, '/auth/token', endpoint='token')
api.add_resource(BucketlistsApi, '/bucketlists/', endpoint='lists')
api.add_resource(BucketlistApi, '/bucketlists/<int:id>', endpoint='list')
api.add_resource(
    BucketlistItemCreateApi, '/bucketlists/<int:id>/items/', endpoint='item_create')
api.add_resource(
    BucketItemsApi, '/bucketlists/<int:id>/items/<int:item_id>', endpoint='item')
