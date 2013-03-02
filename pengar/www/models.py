from datetime import datetime
from passlib.apps import custom_app_context as pengar_pwd_context

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Unicode, ForeignKey, \
        DateTime, Integer

from pengar.database.base import Base

class User(Base):
    id = Column(Integer, primary_key=True)

    email = Column(Unicode, unique=True)
    password = Column(Unicode)

    created = Column(DateTime, default=datetime.now)

    accounts = relationship(
        'Account',
        secondary='accounts_users',
        backref=backref('user', lazy='dynamic'))

    def set_password(self, password):
        self.password = pengar_pwd_context.encrypt(password)

    def check_password(self, password):
        return pengar_pwd_context.verify(password, self.password)

    def __repr__(self):
        return u'<User #{0} {1}>'.format(self.id, self.email)



class AccountsUsers(Base):
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


MODELS = [
    User,
    AccountsUsers
]
