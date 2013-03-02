import logging

from flask import session

from pengar.www.models import User, AccountsUsers
from pengar.models import Account
from pengar.database import db


_log = logging.getLogger(__name__)


class UpdateError(IOError):
    pass


def login_user(user):
    session['user_id'] = user.id


def get_current_user():
    if 'user_id' in session.keys():
        return User.query.filter_by(id=session['user_id']).first()
    else:
        return None


def update_accounts(user_id, ssn, code):
    from pengar.swedbank import Swedbank
    from pengar.util.update import save_transactions

    user = User.query.filter_by(id=user_id).first()

    if not user:
        raise UpdateError('Invalid user id.')

    if not ssn and code:
        raise UpdateError('Missing SSN or code')

    bank = Swedbank(ssn=ssn, code=code)

    try:
        bank.login()
    except AssertionError:
        raise UpdateError('Could not log in, are the SSN and code valid?')

    accounts = bank.get_accounts()

    for bank_account in accounts:
        transactions = bank.get_transactions(bank_account['id'], 100)

        account = Account.query.join(AccountsUsers).join(User)\
                .filter(Account.label == bank_account['name'])\
                .filter(User.id == user).first()

        if not account:
            account = Account(
                label=bank_account['name'],
                amount=bank_account['amount'])


            db.session.add(account)
            db.session.commit()

            au = AccountsUsers(user_id=user.id, account_id=account.id)

            db.session.add(au)
            db.session.commit()

        _log.info('Updating account {0}'.format(account))

        return save_transactions(
            account.id,
            transactions)
    else:
        raise UpdateError('No accounts could be found.')
