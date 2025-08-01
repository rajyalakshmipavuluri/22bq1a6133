db = SQLAlchemy()
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ShortURL(db.Model):
    __tablename__ = 'short_urls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    shortcode = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        # Checks if the shortcode has expired
        return datetime.utcnow() > self.expires_at
