"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from players import Bankroll


class TestBankroll(unittest.TestCase):
    def setUp(self):
        self._bankroll = Bankroll(10_000)

    def tearDown(self):
        pass

    def test_amount(self):
        """ Test bankroll has an amount """
        bankroll = self._bankroll
        self.assertEqual(bankroll.amount, 10_000)

    def test_amount_setter(self):
        """ Test bankroll amount can be set """
        bankroll = self._bankroll
        new_bankroll = 200_000
        bankroll.amount = new_bankroll
        self.assertEqual(bankroll.amount, new_bankroll)

    def test_invest(self):
        """ Test bankroll can be invested in """
        bankroll = self._bankroll
        additional = 1_000
        bankroll.invest(additional)
        self.assertEqual(bankroll.amount, 11_000)

    def test_withdraw(self):
        """ Test bankroll can be withdrawn from """
        bankroll = self._bankroll
        pay_out = 4_000
        bankroll.withdraw(pay_out)
        self.assertEqual(bankroll.amount, 6_000)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
