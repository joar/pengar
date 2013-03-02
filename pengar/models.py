from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, Unicode, DateTime, \
        Boolean, ForeignKey, SmallInteger, Numeric

from pengar.database.base import Base


class Account(Base):
    id = Column(Integer, primary_key=True)
    label = Column(Unicode)
    amount = Column(Numeric)
    transactions = relationship('Transaction', backref=backref('account'))
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return u'<Account #{0} {1}>'.format(
            self.id,
            self.label
        )


class Transaction(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    note = Column(Unicode)
    date = Column(DateTime)
    amount = Column(Numeric)

    def __repr__(self):
        return u'<Transaction #{0} {1} ({2}) on {3}>'.format(
            self.id,
            self.note.encode('ascii', 'replace'),
            int(self.amount),
            self.date.isoformat()
        )


MODELS = [
    Account,
    Transaction,
]
