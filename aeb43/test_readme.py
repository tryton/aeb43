# This file is part of aeb43.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import doctest
import os

here = os.path.dirname(__file__)
readme = os.path.normpath(os.path.join(here, '..', 'README.rst'))


def load_tests(loader, tests, pattern):
    if os.path.isfile(readme):
        tests.addTest(doctest.DocFileSuite(
                readme, module_relative=False,
                encoding='utf-8',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return tests
