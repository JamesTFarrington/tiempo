import redis
from itertools import islice
from .conf import REDIS_HOST, REDIS_PORT, REDIS_QUEUE_DB, REDIS_PW


REDIS = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_QUEUE_DB,
    password=REDIS_PW
)

NOTIFY_PUBSUB = REDIS.pubsub()


def subscribe_to_backend_notifications(db=REDIS_QUEUE_DB):
    REDIS.config_set('notify-keyspace-events', 'KEA')
    NOTIFY_PUBSUB.psubscribe('__keyspace@%s__:results*' % db)
    NOTIFY_PUBSUB.psubscribe('__keyevent@%s__:expired' % db)


def hear_from_backend():
    events = []
    def parse_backend():
        try:
            messages = NOTIFY_PUBSUB.parse_response()
        except AttributeError:
            messages = None
        if messages:
            for message in messages:
                events.append(message)
        return events
    return parse_backend
