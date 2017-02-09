"""
Created on Jan 15, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.shoe import Shoe


class TestShoe(unittest.TestCase):
    def setUp(self):
        self._shoe = Shoe()

    def tearDown(self):
        pass

    def test_shoe_length_single_deck(self):
        """ Test shoe is the correct length for a single deck """
        shoe = self._shoe
        self.assertEqual(len(shoe), 52)

    def test_shoe_length_double_deck(self):
        """ Test shoe is the correct length for a single deck """
        shoe = Shoe(2)
        self.assertEqual(len(shoe), 104)

    def test_shoe_length_four_deck(self):
        """ Test shoe is the correct length for a single deck """
        shoe = Shoe(4)
        self.assertEqual(len(shoe), 208)

    def test_shoe_length_six_deck(self):
        """ Test shoe is the correct length for a single deck """
        shoe = Shoe(6)
        self.assertEqual(len(shoe), 312)

    def test_shoe_length_eight_deck(self):
        """ Test shoe is the correct length for a single deck """
        shoe = Shoe(8)
        self.assertEqual(len(shoe), 416)

    def test_deal_card(self):
        """ Test shoe can deal the top card from the shoe """
        shoe = self._shoe
        card = shoe[0]
        self.assertEqual(len(shoe), 52)
        dealt_card = shoe.deal_card()
        self.assertEqual(len(shoe), 51)
        self.assertEqual(dealt_card, card)

    def test_shuffle(self):
        """ Test shoe can be shuffled """
        shoe = self._shoe
        unshuffled_shoe = [card for card in shoe]
        shoe.shuffle()
        same = 0
        for index, card in enumerate(shoe):
            if card == unshuffled_shoe[index]:
                same += 1
        self.assertLess(same, 5)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
