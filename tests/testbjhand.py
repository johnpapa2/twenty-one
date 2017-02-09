"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from players.bjhand import BjHand
from cards.bjcard import BjCard


class TestBjHand(unittest.TestCase):
    def setUp(self):
        self._hand = BjHand(150)

    def tearDown(self):
        pass

    def test_bet(self):
        """ Test hand has a bet """
        hand = self._hand
        self.assertEqual(hand.bet.amount, 150)

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

    def test_for_splittable_hand(self):
        """ Test bj hand can identify a hand that is allowed to be split """
        hand = self._hand
        cards = [BjCard('clubs', '5'), BjCard('diamonds', '5')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.can_split, True)

    def test_for_splittable_hand_with_ten_value_cards(self):
        """ Test bj hand can identify a hand that is allowed to be split """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'K')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.can_split, True)

    def test_for_splittable_hand_with_aces(self):
        """ Test bj hand can identify a hand that is allowed to be split """
        hand = self._hand
        cards = [BjCard('clubs', 'A'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.can_split, True)

    def test_for_non_splittable_hand(self):
        """ Test bj hand can identify a hand that is not allowed to be split """
        hand = self._hand
        cards = [BjCard('clubs', '7'), BjCard('diamonds', '4')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.can_split, False)

    def test_value(self):
        """ Test bj hand returns the hand value """
        hand = self._hand
        cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 21)

    def test_value_hard_hand(self):
        """ Test bj hand returns the hand value for a hard hand """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('hearts', 'A'), BjCard('clubs', 'K')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 17)

    def test_value_hard_hand_two_aces(self):
        """ Test bj hand returns the hand value for a hard hand with two aces """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('hearts', 'A'), BjCard('clubs', 'K'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 18)

    def test_value_soft_hand(self):
        """ Test bj hand returns the hand value for a soft hand """
        hand = self._hand
        cards = [BjCard('diamonds', '7'), BjCard('hearts', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 18)

    def test_value_soft_hand_two_aces(self):
        """ Test bj hand returns the hand value for a soft hand with two aces """
        hand = self._hand
        cards = [BjCard('spades', '2'), BjCard('hearts', 'A'), BjCard('clubs', '5'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(hand.value, 19)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
