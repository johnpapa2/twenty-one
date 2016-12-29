"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.hand import Hand
from cards.bjcard import BjCard


class TestHand(unittest.TestCase):
    def setUp(self):
        self._hand = Hand()
        self._bet = 150
        self._hand.bet = 150

    def tearDown(self):
        pass

    def test_add_card(self):
        """ Test 'add_card' adds a card to the hand """
        hand = self._hand
        card = BjCard('spades', 'A')
        hand.add_card(card)
        self.assertEqual(len(hand), 1)
        self.assertEqual(hand[0], card)

    def test_bet(self):
        """ Test 'bet' property returns the bet value """
        hand = self._hand
        self.assertEqual(hand.bet, self._bet)

    def test_bet(self):
        """ Test 'bet' setter property sets the bet value """
        hand = self._hand
        new_bet = 200
        hand.bet = new_bet
        self.assertEqual(hand.bet, new_bet)

    def test_dunder_str(self):
        """ Test '__str__' returns the correct hand display """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('clubs', '9')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(str(hand), '[6] [9]')

    def test_value(self):
        """ Test 'value' property returns the hand value """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 21)

    def test_value_soft_hand(self):
        """ Test 'value' property returns the hand value """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('hearts', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 17)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
