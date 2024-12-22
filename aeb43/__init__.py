# This file is part of aeb43.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
"""a parser for AEB43 files
"""
__version__ = '0.1.1'
__all__ = ['AEB43']

import datetime as dt
import io
from decimal import Decimal

from stdnum.es.ccc import calc_check_digits, to_iban


def _parse_date(date):
    return dt.datetime.strptime(date, '%y%m%d').date()


class AEB43:

    def __init__(self, name, encoding=None):
        self.accounts = []

        if isinstance(name, (bytes, str)):
            with io.open(name, encoding=encoding, mode='r') as f:
                self._parse(f)
        else:
            self._parse(name)

    def _parse(self, f):
        account = transaction = None
        count = 0
        for line in self._readline(f):
            code = line[:2]
            if code == '00':
                self._parse_file_header(line)
            elif code == '11':
                count += 1
                account = Account()
                self.accounts.append(account)
                self._parse_account_header(line, account)
            elif code == '22':
                count += 1
                transaction = Transaction()
                account.transactions.append(transaction)
                self._parse_transaction(line, transaction)
            elif code == '23':
                count += 1
                self._parse_transaction_optional_item(line, transaction)
            elif code == '33':
                count += 1
                self._parse_account_end(line, account)
                account = transaction = None
            elif code == '88':
                assert count == int(line[20:26])
                account = transaction = None
                break

    @staticmethod
    def _readline(f):
        for line in f:
            yield line

    def _parse_file_header(self, line):
        self.bank_code = line[2:6]
        self.accounting_date = _parse_date(line[6:12])

    def _parse_account_header(self, line, account):
        account.bank_code = line[2:6]
        account.branch_code = line[6:10]
        account.number = line[10:20]
        account.start_date = _parse_date(line[20:26])
        account.end_date = _parse_date(line[26:32])
        sign = {
            '1': -1,
            '2': 1,
            }[line[32]]
        account.initial_balance = sign * Decimal(line[33:47]) / 100
        account.currency = line[47:50]
        account.name = line[51:77].strip()
        account.code = line[77:80]

    def _parse_transaction(self, line, transaction):
        transaction.branch_code = line[6:10]
        transaction.transaction_date = _parse_date(line[10:16])
        transaction.value_date = _parse_date(line[16:22])
        transaction.shared_item = line[22:24]
        transaction.own_item = line[24:27]
        sign = {
            '1': -1,
            '2': 1,
            }[line[27]]
        transaction.amount = sign * Decimal(line[28:42]) / 100
        transaction.document = line[42:52]
        transaction.reference1 = line[52:64]
        transaction.reference2 = line[64:80]

    def _parse_transaction_optional_item(self, line, transaction):
        transaction.items.append(line[4:42].strip())
        transaction.items.append(line[42:80].strip())

    def _parse_account_end(self, line, account):
        assert account.bank_code == line[2:6]
        assert account.branch_code == line[6:10]
        assert account.number == line[10:20]
        assert account.number_of_debit == int(line[20:25])
        assert account.total_debit == Decimal(line[25:39]) / 100
        assert account.number_of_credit == int(line[39:44])
        assert account.total_credit == Decimal(line[44:58]) / 100
        sign = {
            '1': -1,
            '2': 1,
            }[line[58]]
        account.final_balance = sign * Decimal(line[59:73]) / 100
        assert account.currency == line[73:76]

        assert (
            account.initial_balance
            - account.total_debit
            + account.total_credit) == account.final_balance


class _SlotsNone:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.__slots__:
            setattr(self, name, None)


class Account(_SlotsNone):
    __slots__ = (
        'bank_code', 'branch_code', 'number', 'start_date', 'end_date',
        'initial_balance', 'final_balance', 'currency', 'name', 'code',
        'transactions')

    def __init__(self):
        super().__init__()
        self.transactions = []

    @property
    def client_account_code(self):
        check = calc_check_digits(
            self.bank_code + self.branch_code + '00' + self.number)
        return self.bank_code + self.branch_code + check + self.number

    ccc = client_account_code

    @property
    def iban(self):
        return to_iban(self.client_account_code)

    @property
    def number_of_debit(self):
        return len([t for t in self.transactions if t.amount < 0])

    @property
    def total_debit(self):
        return -sum((t.amount for t in self.transactions if t.amount < 0))

    @property
    def number_of_credit(self):
        return len([t for t in self.transactions if t.amount > 0])

    @property
    def total_credit(self):
        return sum((t.amount for t in self.transactions if t.amount > 0))


class Transaction(_SlotsNone):
    __slots__ = (
        'branch_code', 'transaction_date', 'value_date', 'shared_item',
        'own_item', 'amount', 'document', 'reference1', 'reference2', 'items')

    def __init__(self):
        super().__init__()
        self.items = []
