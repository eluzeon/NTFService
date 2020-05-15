from uuid import uuid4
from flask_cqlalchemy import CQLAlchemy
from datetime import datetime

db = CQLAlchemy()


def days_to_sec(days):
    return days * 24 * 60 * 60

# Default notification Time to Live (in sec);
TTL = days_to_sec(14)
PAGE_BY = 20


class Notification(db.Model):
    id = db.columns.UUID(default=uuid4, primary_key=True)
    message = db.columns.Text()
    img_url = db.columns.Text(required=False)

    options = {
        "default_time_to_live": TTL
    }


class UserNotification(db.Model):
    nid = db.columns.UUID()
    user_id = db.columns.Integer(primary_key=True, partition_key=True)
    lesson_id = db.columns.Integer(required=False)
    # control scheduled notifications
    # set `datetime.now` if show notification immediately.
    # also used for sorting notifications
    show_after = db.columns.DateTime(primary_key=True, default=datetime.utcnow)
    read = db.columns.Boolean(default=False)

    def __init__(self, *args, **kwargs):
        super(UserNotification, self).__init__(*args, **kwargs)
        self.notification = None

    options = {
        "default_time_to_live": TTL
    }
