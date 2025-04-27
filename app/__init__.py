import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_restful import Api

from .config import Config, config_by_name

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api_restful = Api()

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')  
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from .views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    @app.route('/ping')
    def ping():
        return jsonify({"message": "pong"})

    return app