from pengar.swedbank import Swedbank


def main():
    bank = Swedbank()
    bank.login()

    accounts = bank.get_accounts()
    print(accounts)

    transactions = bank.get_transactions(1, 3)
    print(transactions)
