"""
Created on Dec 29, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.deck import Deck


class TestDeck(unittest.TestCase):
    def setUp(self):
        self._deck = Deck()

    def tearDown(self):
        pass

    def test_deal_card(self):
        """ Test deck can deal the top card from the deck """
        deck = self._deck
        card = deck[0]
        self.assertEqual(len(deck), 52)
        dealt_card = deck.deal_card()
        self.assertEqual(len(deck), 51)
        self.assertEqual(dealt_card, card)

    def test_shuffle(self):
        """ Test the deck can be shuffled """
        deck = self._deck
        unshuffled_deck = [card for card in deck]
        deck.shuffle()
        same = 0
        for index, card in enumerate(deck):
            if card == unshuffled_deck[index]:
                same += 1
        self.assertLess(same, 5)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
