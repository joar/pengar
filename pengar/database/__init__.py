import logging

import config

from sqlalchemy import create_engine

from .base import Base, Session

_log = logging.getLogger(__name__)


class DatabaseMaster(object):
    '''
    From mediagoblin/db/open.py
    '''
    def __init__(self, engine):
        self.engine = engine
        self.session = Session

        for k, v in Base._decl_class_registry.iteritems():
            setattr(self, k, v)

    def commit(self):
        Session.commit()

    def save(self, obj):
        Session.add(obj)
        Session.flush()


def set_up_database(config):
    engine = create_engine(config.DATABASE_URL)

    Session.configure(bind=engine)

    return DatabaseMaster(engine)

db = set_up_database(config)
