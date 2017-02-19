"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from players import Hand
from cards import BjCard


class TestHand(unittest.TestCase):
    def setUp(self):
        self._hand = ConcreteHand()

    def tearDown(self):
        pass

    def test_add_card(self):
        """ Test hand can have a card added to it """
        hand = self._hand
        card = BjCard('spades', 'A')
        hand.add_card(card)
        self.assertEqual(len(hand), 1)
        self.assertEqual(hand[0], card)

    def test_dunder_str(self):
        """ Test hand can be displayed correctly """
        hand = self._hand
        cards = [BjCard('spades', '6'), BjCard('clubs', '9')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(str(hand), '[6] [9]')

    def test_hand_is_abstract_class(self):
        """ Test that the Hand class is an abstract base class """
        with self.assertRaises(TypeError):
            Hand()

    def test_remove_card(self):
        """ Test hand can have a card removed from it (for splitting hands) """
        hand = self._hand
        cards = [BjCard('hearts', 'A'), BjCard('diamonds', 'A')]
        for card in cards:
            hand.add_card(card)
        self.assertEqual(len(hand), 2)
        card = hand.remove_card(1)
        self.assertEqual(card.value, 11)
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'diamonds')
        self.assertEqual(len(hand), 1)


class ConcreteHand(Hand):
    def __init__(self):
        super().__init__()

    def value(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
