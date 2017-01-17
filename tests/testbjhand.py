"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.bjhand import BjHand
from cards.bjcard import BjCard


class TestBjHand(unittest.TestCase):
    def setUp(self):
        self._hand = BjHand()
        self._bet = 150
        self._hand.bet = 150

    def tearDown(self):
        pass

    def test_for_blackjack(self):
        """ Test bj hand can identify a natural blackjack """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.is_blackjack, True)

    def test_for_non_blackjack(self):
        """ Test bj hand can identify a non blackjack hand """
        hand = self._hand
        cards = [BjCard('clubs', '8'), BjCard('diamonds', '8')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.is_blackjack, False)

    def test_value(self):
        """ Test bj hand returns the hand value """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 21)

    def test_value_soft_hand(self):
        """ Test bj hand returns the hand value for a soft hand """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('hearts', 'A'), BjCard('clubs', 'K')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 17)

    def test_value_soft_hand_two_aces(self):
        """ Test bj hand returns the hand value for a soft hand with two aces """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('hearts', 'A'), BjCard('clubs', 'K'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 18)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
