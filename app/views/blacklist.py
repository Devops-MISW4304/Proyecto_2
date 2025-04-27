from functools import wraps
from flask import request, current_app
from flask_restful import Resource
from marshmallow import ValidationError

from .. import db
from ..models.blacklist import BlacklistEntry
from ..schemas.blacklist import BlacklistSchema, blacklist_creation_schema

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token_type, token = auth_header.split()
                if token_type.lower() != 'bearer':
                    token = None
            except ValueError:
                token = None

        if not token or token != current_app.config.get('STATIC_BEARER_TOKEN'):
            return {'message': 'Token invalido'}, 401

        return f(*args, **kwargs)
    return decorated


class BlacklistResource(Resource):
    """Endpoint para obtener todas las entradas y crear una nueva."""

    @token_required
    def get(self):
        # Get all blacklist 
        entries = BlacklistEntry.query.all()
        schema = BlacklistSchema(many=True)
        result = schema.dump(entries)
        return {"blacklists": result}, 200

    @token_required
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No data insertada"}, 400

        try:
            data = blacklist_creation_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        existing_entry = BlacklistEntry.query.filter_by(email=data.email).first()
        if existing_entry:
            return {'message': f'Email {data.email} ya se encuentra en la blacklist'}, 409

        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr

        new_entry = BlacklistEntry(
            email=data.email,
            app_uuid=data.app_uuid,
            blocked_reason=data.blocked_reason,
            ip_address=ip_address
        )

        try:
            db.session.add(new_entry)
            db.session.commit()
            return {'message': f'Email {new_entry.email} añadida a la blacklist correctamente.'}, 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al insertar email en la blacklist: {e}")
            return {"message": "Internal server error while adding email"}, 500


class BlacklistDetailResource(Resource):
    """Endpoint para obtener una entrada de la blacklist filtrada por email."""

    @token_required
    def get(self, email):
        entry = BlacklistEntry.query.filter_by(email=email).first()
        print("Cambio sencillo v3 para probar ejecución del pipeline Codebuild")
        
        if not entry:
            return {"is_blacklisted": False, "blocked_reason": None}, 200
        
        
        return {"is_blacklisted": True, "blocked_reason": entry.blocked_reason}, 200
