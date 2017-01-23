import uuid
import hmac
import os
from hashlib import sha1

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.core.urlresolvers import reverse

import redis


class RedisManager(object):

    def __init__(self, *args, **kwargs):
        self.db_name = kwargs.get('db_name')
        self.connection = self._connection()

    def keys(self, v):
        return self.connection.keys(v)

    def _connection(self):
        return redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT,
            db=settings.REDIS_DB[self.db_name])

    def get(self, key):
        return self.connection.get(key)

    def setex(self, k, v, time=600):
        return self.connection.setex(k, time, v)


redis_auth_db = RedisManager(db_name='auth')


def content_to_template_render(content, **kwargs):
    template = Template(content)
    ctx = Context(kwargs)
    return template.render(ctx)


def _send_email(subject, content, from_email, recipient_list):
    client = EmailMultiAlternatives(
        subject, content, from_email, recipient_list)
    client.attach_alternative(content, "text/html")
    return client.send()


def generate_key(size=10):
    unique = uuid.uuid4()
    return hmac.new(unique.bytes, digestmod=sha1).hexdigest()[:size]


def generate_password_reset_url(recipient_list, http_host, http_schema):
    token = generate_key()
    email = recipient_list[0]
    redis_auth_db.setex(token, email)

    set_password_url = reverse('account:password-reset',
                               kwargs={'token': token})
    return "{http_schema}://{http_host}{set_password_url}".format(
        http_schema=http_schema, http_host=http_host,
        set_password_url=set_password_url)


def template_exists(template_path):
    for path in settings.TEMPLATE_DIRS:
        file_path = os.path.join(path, template_path)
        if os.path.exists(file_path):
            return file_path


def send_email(sender_payload):
    template_path = template_exists(
        sender_payload.content_template)
    _file = open(template_path)
    content = _file.read()
    _file.close()
    password_reset_url = generate_password_reset_url(
        sender_payload.recipient_tuple,
        sender_payload.http_host, sender_payload.http_schema)
    template = content_to_template_render(
        content, password_reset_url=password_reset_url)
    return _send_email(
        template, sender_payload.subject, sender_payload.from_email,
        sender_payload.recipient_tuple)
