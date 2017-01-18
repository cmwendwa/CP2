from app import app, db
from app.models import User, Item, Bucketlist
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
api = Api(app=app, prefix='/api/v1')

from app.api_v1.resources import RegisterApi, LoginApi, BucketlistsApi, BucketlistApi, BucketItemsApi, BucketlistItemCreateApi, IndexResource


api.add_resource(RegisterApi, '/auth/register', endpoint='register')
api.add_resource(LoginApi, '/auth/login', endpoint='login')
api.add_resource(BucketlistsApi, '/bucketlists/', endpoint='lists')
api.add_resource(BucketlistApi, '/bucketlists/<int:id>', endpoint='list')
api.add_resource(
    BucketlistItemCreateApi, '/bucketlists/<int:id>/items/', endpoint='item_create')
api.add_resource(
    BucketItemsApi, '/bucketlists/<int:id>/items/<int:item_id>', endpoint='item')
api.add_resource(
    IndexResource, '/', endpoint='index')


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """Add app, database and models to the shell."""
    return dict(app=app, db=db, User=User, Bucketlist=Bucketlist,
                Item=Item)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
