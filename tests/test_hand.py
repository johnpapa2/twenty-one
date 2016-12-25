"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.hand import Hand
from cards.bjcard import BjCard


class Test_Hand(unittest.TestCase):
    def setUp(self):
        self._hand = Hand()

    def tearDown(self):
        pass

    def test_add_card(self):
        """ Test 'add_card' adds a card to the hand """
        hand = self._hand
        card = BjCard('spades', 'A')
        hand.add_card(card)
        self.assertEqual(len(hand), 1)
        self.assertEqual(hand[0], card)

    def test_value(self):
        """ Test 'value' property returns the hand value """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 21)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
