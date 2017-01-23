from collections import namedtuple


EmailSenderTuple = namedtuple(
    'EmailSenderTuple',
    'subject content_template from_email recipient_tuple \
     http_host http_schema')
