# This file is part of aeb43.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
"""Test AEB43
"""
import datetime as dt
import io
import os
import unittest
from decimal import Decimal

from aeb43 import AEB43

here = os.path.dirname(__file__)


class TestAEB43(unittest.TestCase):

    def setUp(self):
        self.aeb43 = AEB43(os.path.join(here, 'AEB43.txt'))

    def test_number_accounts(self):
        "Test number of accounts"
        self.assertEqual(len(self.aeb43.accounts), 1)

    def test_account(self):
        "Test account"
        account = self.aeb43.accounts[0]
        self.assertEqual(account.bank_code, '0081')
        self.assertEqual(account.branch_code, '5398')
        self.assertEqual(account.number, '0001414452')
        self.assertEqual(account.start_date, dt.date(2018, 3, 18))
        self.assertEqual(account.end_date, dt.date(2018, 3, 20))
        self.assertEqual(account.initial_balance, Decimal('3005.00'))
        self.assertEqual(account.final_balance, Decimal('2994.02'))
        self.assertEqual(account.currency, '978')
        self.assertEqual(account.name, 'DUNDER MIFFLIN')
        self.assertEqual(account.code, '   ')
        self.assertEqual(account.client_account_code, '00815398730001414452')
        self.assertEqual(account.iban, 'ES0600815398730001414452')

    def test_number_transactions(self):
        "Test number of transactions"
        account = self.aeb43.accounts[0]
        self.assertEqual(len(account.transactions), 1)

    def test_transaction(self):
        "Test transaction"
        account = self.aeb43.accounts[0]
        transaction = account.transactions[0]
        self.assertEqual(transaction.branch_code, '0901')
        self.assertEqual(transaction.transaction_date, dt.date(2018, 3, 19))
        self.assertEqual(transaction.value_date, dt.date(2018, 3, 19))
        self.assertEqual(transaction.shared_item, '12')
        self.assertEqual(transaction.own_item, '408')
        self.assertEqual(transaction.amount, Decimal('-10.98'))
        self.assertEqual(transaction.document, '0' * 10)
        self.assertEqual(transaction.reference1, '0' * 12)
        self.assertEqual(transaction.reference2, '5540014387733014')
        self.assertEqual(
            transaction.items,
            ['COMPRA TARG 5540XXXXXXXX3014 DNH*MICHA', 'EL SCOTT'])


class TestAEB43Stream(TestAEB43):

    def setUp(self):
        with io.open(os.path.join(here, 'AEB43.txt')) as f:
            self.aeb43 = AEB43(f)
