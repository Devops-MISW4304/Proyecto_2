from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class BlacklistEntry(db.Model):
    __tablename__ = 'blacklist_entries'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlacklistEntry {self.email}>'