from datetime import datetime
from operator import attrgetter
from typing import List
from uuid import uuid4, UUID
from .models import Notification, UserNotification
from base64 import b64encode, b64decode
import pytz


def tokenize_timestamp(ts):
    return b64encode(str(ts).encode('utf-8')).decode('utf-8')


def parse_token(token):
    return datetime.utcfromtimestamp(float(b64decode(token.encode('utf-8'))))


def for_user(user_id: int, fetch_notifications=False, page_token=None):
    td = datetime.utcnow()
    usr = UserNotification\
        .filter(user_id=user_id)\
        .order_by('-show_after')\
        .limit(2)
    if page_token:
        usr = usr.filter(show_after__lt=parse_token(page_token))
    else:
        usr = usr.filter(show_after__lte=td)
    # prefetch related notifications
    if fetch_notifications:
        related_ntfs = Notification.filter(id__in=list(map(attrgetter('nid'), usr)))
        for n in usr:
            ntf = list(filter(lambda x: x.id == n.nid, related_ntfs))[0]
            n.notification = ntf
    return usr, (tokenize_timestamp(pytz.utc.localize(usr[-1].show_after).timestamp()) if len(usr) else None)


def row_ttl(ttl: int, delay: datetime = None):
    delay = delay.timestamp() if delay else 0
    return ttl + delay


def create_notification(user_ids: List[int],
                        message: str,
                        img_url: str = None,
                        delay: datetime = None,
                        lesson_id: int = None,
                        ttl: int = None):
    NotifPrep = Notification
    UserNotifPrep = UserNotification
    if ttl:
        # provide ttl if custom expire provided
        # otherwise use model's default ttl
        ttl = row_ttl(ttl, delay)
        NotifPrep = NotifPrep.ttl(ttl)
        UserNotifPrep = UserNotifPrep.ttl(ttl)
    ntf = NotifPrep.create(id=uuid4(), message=message, img_url=img_url)
    show_after = delay
    if not show_after:
        show_after = datetime.utcnow()
    for u in user_ids:
        UserNotifPrep.create(
            nid=ntf.id, user_id=u,
            lesson_id=lesson_id, show_after=show_after)
    return ntf


def read_notification(nid: UUID, user_id: int):
    UserNotification.filter(nid=nid, user_id=user_id)