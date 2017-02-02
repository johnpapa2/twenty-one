"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from players.bet import Bet


class TestBet(unittest.TestCase):
    def setUp(self):
        self._bet = Bet(75)

    def tearDown(self):
        pass

    def test_amount(self):
        """ Test bet has an amount """
        bet = self._bet
        self.assertEqual(bet.amount, 75)

    def test_amount_setter(self):
        """ Test bet amount can be set """
        bet = self._bet
        new_bet = 200
        bet.amount = new_bet
        self.assertEqual(bet.amount, new_bet)

    def test_increase_amount(self):
        """ Test bet amount can be increased """
        bet = self._bet
        additional = 100
        bet.increase(additional)
        self.assertEqual(bet.amount, 175)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
