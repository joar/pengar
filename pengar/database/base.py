import re

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy import Column

Session = scoped_session(sessionmaker())

_camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')

class _BoundDeclarativeMeta(DeclarativeMeta):
    '''
    From flask-sqlalchemy
    '''

    def __new__(cls, name, bases, d):
        tablename = d.get('__tablename__')

        # generate a table name automatically if it's missing and the
        # class dictionary declares a primary key. We cannot always
        # attach a primary key to support model inheritance that does
        # not use joins. We also don't want a table name if a whole
        # table is defined
        if not tablename and d.get('__table__') is None and \
           _defines_primary_key(d):
            def _join(match):
                word = match.group()
                if len(word) > 1:
                    return ('_%s_%s' % (word[:-1], word[-1])).lower()
                return '_' + word.lower()
            d['__tablename__'] = _camelcase_re.sub(_join, name).lstrip('_')

        return DeclarativeMeta.__new__(cls, name, bases, d)

    def __init__(self, name, bases, d):
        bind_key = d.pop('__bind_key__', None)
        DeclarativeMeta.__init__(self, name, bases, d)
        if bind_key is not None:
            self.__table__.info['bind_key'] = bind_key

class PengarBaseModel(object):
    query = Session.query_property()

def _defines_primary_key(d):
    """Figures out if the given dictonary defines a primary key column."""
    return any(v.primary_key for k, v in d.iteritems()
               if isinstance(v, Column))

Base = declarative_base(
    cls=PengarBaseModel,
    metaclass=_BoundDeclarativeMeta)
