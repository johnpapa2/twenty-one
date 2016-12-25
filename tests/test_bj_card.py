"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from cards.bjcard import BjCard


class Test_BJ_Card(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_value_number(self):
        """ Test 'value' property returns correct value for card ranks 2 - 10. """
        card = BjCard('spades', '2')
        self.assertEqual(card.value, 2)

    def test_value_face(self):
        """ Test 'value' property returns correct value for face cards J Q K. """
        card = BjCard('spades', 'J')
        self.assertEqual(card.value, 10)

    def test_value_ace(self):
        """ Test 'value' property returns correct value for card rank Ace. """
        card = BjCard('spades', 'A')
        self.assertEqual(card.value, 11)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
