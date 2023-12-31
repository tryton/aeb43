aeb43
=====

aeb43 is a parser for AEB43 files.

Nutshell
--------

Import::

    >>> import os
    >>> from aeb43 import AEB43

Instantiate::

    >>> aeb43 = AEB43('aeb43/AEB43.txt')

The accounts::

    >>> len(aeb43.accounts)
    1
    >>> account = aeb43.accounts[0]
    >>> account.number
    '0001414452'
    >>> account.start_date
    datetime.date(2018, 3, 18)
    >>> account.end_date
    datetime.date(2018, 3, 20)
    >>> account.initial_balance
    Decimal('3005')
    >>> account.final_balance
    Decimal('2994.02')
    >>> account.currency
    '978'

The transactions::

    >>> len(account.transactions)
    1
    >>> transaction = account.transactions[0]
    >>> transaction.transaction_date
    datetime.date(2018, 3, 19)
    >>> transaction.value_date
    datetime.date(2018, 3, 19)
    >>> transaction.amount
    Decimal('-10.98')
    >>> transaction.shared_item
    '12'
    >>> transaction.own_item
    '408'
    >>> transaction.document
    '0000000000'
    >>> transaction.reference1
    '000000000000'
    >>> transaction.reference2
    '5540014387733014'
    >>> transaction.items
    ['COMPRA TARG 5540XXXXXXXX3014 DNH*MICHA', 'EL SCOTT']

To report issues please visit the `aeb43 bugtracker`_.

.. _aeb43 bugtracker: https://bugs.tryton.org/aeb43
