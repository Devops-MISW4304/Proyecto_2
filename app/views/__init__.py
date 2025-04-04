from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from . import blacklist

api.add_resource(blacklist.BlacklistResource, '/blacklists', endpoint='blacklists_post')
api.add_resource(blacklist.BlacklistDetailResource, '/blacklists/<string:email>', endpoint='blacklist_detail')
