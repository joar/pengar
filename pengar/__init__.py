import logging
from . import swedbank

_log = logging.getLogger(__name__)

def main():
    # Set up logging
    logging.basicConfig()
    _log.setLevel(logging.INFO)

    bank = swedbank.Swedbank()
    bank.login()

    accounts = bank.get_accounts()
    print(accounts)

    transactions = bank.get_transactions(1, 3)
    print(transactions)

if __name__ == '__main__':
    main()
