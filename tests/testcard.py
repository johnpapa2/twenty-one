"""
Created on Dec 04, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.card import Card


class TestCard(unittest.TestCase):
    def setUp(self):
        self._suit = "clubs"
        self._rank = "10"
        self._card = ConcreteCard(suit=self._suit, rank=self._rank)

    def tearDown(self):
        pass

    def test_card_is_abstract_class(self):
        """ Test that the Card class is an abstract base class """
        with self.assertRaises(TypeError):
            Card()

    def test_rank(self):
        """ Test card has correct rank. """
        card = self._card
        self.assertEqual(card.rank, self._rank)

    def test_suit(self):
        """ Test card has correct suit. """
        card = self._card
        self.assertEqual(card.suit, self._suit)


class ConcreteCard(Card):
    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    @property
    def value(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
