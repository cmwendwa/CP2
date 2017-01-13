from flask import Flask, jsonify
from flask_restful import Api
from config import config
from flask_sqlalchemy import SQLAlchemy
import os
from flask import send_from_directory


db = SQLAlchemy()


def create_app(config_choice):
    app = Flask(__name__)
    app.config.from_object(config[config_choice])
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()  # this does the binding

    @app.errorhandler(410)
    def gone(e):
        return jsonify(error=410, text=str(e)), 410

    @app.errorhandler(409)
    def gone(e):
        return jsonify(error=409, text=str(e)), 409

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return jsonify(error=404, message=str(e)), 404

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify(error=403, message=str(e)), 403
    @app.errorhandler(401)
    def page_not_found(e):
        return jsonify(error=401, text=str(e)), 401

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(error=500, message=str(e)), 500
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.png')

    return app


app = create_app('development')

api = Api(app=app, prefix='/api/v1')


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/pp.db'
