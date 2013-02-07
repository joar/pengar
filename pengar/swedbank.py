import requests
import getpass
import re
import logging
import urlparse
from datetime import datetime

from bs4 import BeautifulSoup

_log = logging.getLogger(__name__)

class Swedbank(object):
    urls = {
        'login': 'https://mobilbank.swedbank.se/banking/swedbank/login.html',
        'loginNext':
            'https://mobilbank.swedbank.se/banking/swedbank/loginNext.html',
        'accounts':
            'https://mobilbank.swedbank.se/banking/swedbank/accounts.html',
        'account':
            'https://mobilbank.swedbank.se/banking/swedbank/account.html?id={0}'
    }
    def __init__(self, **kw):
        self.ssn = kw.get('ssn') or raw_input('Social security number: ')
        self.code = kw.get('code') or getpass.getpass('Passcode: ')

        self.auth_method = 'code'

        self.session = requests.Session()
        self.logged_in = False

    csrf_pattern = re.compile(
        r'<input(.*?)name="_csrf_token".*?value="(?P<token>[^"]*?)"')

    def _parse_csrftoken(self, page_content):
        matches = self.csrf_pattern.search(page_content)
        return matches.groupdict()['token']

    def login(self):
        # Get CSRF token
        _log.info('Requesting CSRF token...')
        token_req = self.session.get(self.urls['login'])

        csrf_token = self._parse_csrftoken(token_req.text)
        _log.debug('CSRF token: {0}'.format(csrf_token))

        _log.info('Submitting SSN login form...')
        login_req = self.session.post(
            self.urls['loginNext'],
            data={
                'xyz': self.ssn,
                'auth-method': self.auth_method,
                '_csrf_token': csrf_token
                })
        _log.debug(login_req.text)

        csrf_token = self._parse_csrftoken(login_req.text)
        _log.debug('CSRF token: {0}'.format(csrf_token))

        _log.info('Submitting code...')
        code_req = self.session.post(
            self.urls['login'],
            data={
                'zyx': self.code,
                '_csrf_token': csrf_token
            }
        )
        _log.debug(code_req.text)

        assert 'https://mobilbank.swedbank.se/banking/swedbank/menu.html?' \
                in code_req.url, 'Login failed'

        self.logged_in = True

    def _parse_numeric(self, string):
        number = _comma_re.sub('.', string)
        return _space_re.sub('', number)

    def get_accounts(self):
        if not self.logged_in:
            raise RuntimeError('Not logged in')

        _log.info('Requesting accounts...')
        accounts_req = self.session.get(self.urls['accounts'])
        _log.debug(accounts_req.text)

        soup = BeautifulSoup(accounts_req.text)

        self.accounts = []

        for dd in soup.dl.find_all('dd'):
            account = {
                'name': dd.find('span', 'name').string.strip(),
                'amount': self._parse_numeric(
                    dd.find('span', 'amount').string.strip())
            }


            link = urlparse.urlparse(dd.find('a').get('href'))

            query = urlparse.parse_qs(link.query)

            account.update({'id': int(query['id'][0])})

            self.accounts.append(account)

        return self.accounts

    def get_transactions(self, account_id, pages=1):
        if not self.logged_in:
            raise RuntimeError('Not logged in')

        transactions = []

        for i in range(1, pages + 1):
            _log.info('Requesting account {0}, page {1}'.format(
                account_id,
                i))

            url = self.urls['account'].format(account_id)

            if i > 1:
                url += '&action=next'

            account_res = self.session.get(url)
            _log.debug(account_res.text)

            transactions.extend(self._parse_transactions(account_res.text))

            if not 'N&auml;sta' in account_res.text:
                _log.info('Reached end of available history. Stopping.')
                break

        return transactions

    def _parse_transactions(self, content):
        soup = BeautifulSoup(content)
        transactions = []

        for dd in soup.find_all('dl')[-1].find_all('dd'):
            transaction = {
                'date': datetime.strptime(
                    dd.find('span', 'date').string.strip(),
                    '%y-%m-%d'),
                'note': dd.find('span', 'receiver').string.strip(),
                'amount': self._parse_numeric(
                    dd.find('span', 'amount').string.strip())
            }
            transactions.append(transaction)

        return transactions

_comma_re = re.compile(r',')
_space_re = re.compile(r' ')


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig()
    _log.setLevel(logging.INFO)

    bank = Swedbank()
    bank.login()

    accounts = bank.get_accounts()
    print(accounts)

    transactions = bank.get_transactions(1, 3)
    print(transactions)
