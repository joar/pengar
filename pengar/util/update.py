import logging

from pengar.models import Transaction, Account
from pengar.database import db

_log = logging.getLogger(__name__)


def intersect_transactions(account_id, transactions):
    account = Account.query.filter(Account.id == account_id).first()

    if account is None:
        raise ValueError(
            u'Account #{0} does not exist in the database'.format(account_id))

    existing = [
        (t.date, t.note, int(t.amount)) for t in
        Transaction.query.filter(Transaction.account_id == Account.id).all()
    ]

    new_transactions = []

    for t in transactions:
        if not (t['date'], t['note'], int(t['amount'])) in existing:
            new_transactions.append(t)

    _log.debug('intersect - new transactions: {0}'.format(new_transactions))

    return new_transactions


def save_transactions(account_id, transactions):
    account = Account.query.filter(Account.id == account_id).first()

    assert account is not None, \
            'Couldn\'t find account with id {0}'.format(account_id)

    _log.debug('save - account: {0}'.format(transactions))

    transactions = intersect_transactions(account.id, transactions)

    _log.debug('save - new transactions: {0}'.format(transactions))

    for t in transactions:
        transaction = Transaction(
            account_id=account.id,
            note=t['note'],
            date=t['date'],
            amount=t['amount'])

        db.session.add(transaction)
        db.session.commit()

    return len(transactions)
