from pengar.swedbank import Swedbank
from pengar.models import Account, Transaction
from pengar.database import db


def main():
    bank = Swedbank()

    bank.login()

    accounts = bank.get_accounts()

    if len(accounts) > 1:
        for account in accounts:
            print(u'{id}: {label} ({amount})'.format(
                id=account['id'],
                label=account['name'],
                amount=account['amount']
            ))

        account_id = int(raw_input('Select an account: '))
    elif len(accounts) == 1:
        account_id = 0
    else:
        return u'No accounts found.'

    pages = int(raw_input(
        'How many pages of transactions do you want to fetch?: '))

    transactions = bank.get_transactions(account_id, pages)

    if len(transactions):
        print(u'Received {0} transactions'.format(len(transactions)))

    proceed = raw_input(
        'Do you want to proceed to write the transactions to'
        ' the local database? [Y/n]: ')

    if proceed.lower() == 'y':
        account = Account(
            label=accounts[account_id]['name'],
            amount=accounts[account_id]['amount'])

        db.session.add(account)
        db.session.commit()

        for t in transactions:
            transaction = Transaction(
                account_id=account.id,
                note=t['note'],
                date=t['date'],
                amount=t['amount'])

            db.session.add(transaction)
            db.session.commit()

        print('Wrote {0} transactions to the database'.format(
            len(transactions)))
