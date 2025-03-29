from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_restful import Api

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api_restful = Api()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    from .views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    @app.route('/ping')
    def ping():
        return jsonify({"message": "pong"})

    return app