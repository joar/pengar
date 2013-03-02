from pengar.swedbank import Swedbank
from pengar.util.update import save_transactions
from pengar.models import Account
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
        account_data = accounts[account_id]

        account = Account.query.filter(Account.label == account_data['name']).first()

        if account is None:
            account = Account(
                label=account_data['name'],
                amount=account_data['amount'])

            db.session.add(account)
            db.session.commit()

        saved_transactions = save_transactions(
            account.id,
            transactions)

        print('Wrote {0} transactions to the database'.format(
            saved_transactions))
