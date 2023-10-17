from datetime import datetime

from . import db
from .constants import MAX_LINK_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String)
    short = db.Column(db.String(MAX_LINK_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
