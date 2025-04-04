from marshmallow import fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from email_validator import validate_email, EmailNotValidError

from .. import ma, db
from ..models.blacklist import BlacklistEntry

def validate_email_address(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValidationError(str(e))

class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlacklistEntry
        load_instance = True
        sqla_session = db.session  # Se asigna la sesión de SQLAlchemy

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate_email_address)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    ip_address = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


blacklist_creation_schema = BlacklistSchema()
