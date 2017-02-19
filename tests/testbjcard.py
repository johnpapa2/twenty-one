"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards import BjCard


class TestBjCard(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_value_number(self):
        """ Test blackjack card has correct value for card ranks 2 - 10. """
        card = BjCard('spades', '2')
        self.assertEqual(card.value, 2)

    def test_value_face(self):
        """ Test blackjack card has correct value for face cards J Q K. """
        card = BjCard('spades', 'J')
        self.assertEqual(card.value, 10)

    def test_value_ace(self):
        """ Test blackjack card has correct value for card rank Ace. """
        card = BjCard('spades', 'A')
        self.assertEqual(card.value, 11)

    def test_set_ace_low(self):
        """ Test blackjack card can set an Ace to a value of 1. """
        card = BjCard('spades', 'A')
        self.assertEqual(card.value, 11)
        card.set_ace_low()
        self.assertEqual(card.value, 1)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
