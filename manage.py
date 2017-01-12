from app import app, db
from app.models import User, Item, Bucketlist
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

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
