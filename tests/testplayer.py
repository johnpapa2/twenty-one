"""
Created on Dec 29, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import unittest

from players.player import Player
from cards.bjcard import BjCard
from click.testing import CliRunner


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self._player = Player('John', 'Player')
        self._cards = [BjCard('clubs', '10'), BjCard('diamonds', 'A')]
        for card in self._cards:
            self._player.hand.add_card(card)

    def tearDown(self):
        pass

    def test_bankroll(self):
        """ Test player has a bankroll """
        player = self._player
        self.assertEqual(player.bankroll.amount, 1000)

    def test_bankroll_setter(self):
        """ Test player can set the bankroll value """
        player = self._player
        player.bankroll.amount = 5250
        self.assertEqual(player.bankroll.amount, 5250)

    def test_bet(self):
        """ Test player has a bankroll """
        player = self._player
        self.assertEqual(player.bet.amount, 0)

    def test_place_bet(self):
        """ Test player can set the bankroll value """
        player = self._player
        player.place_bet(250)
        self.assertEqual(player.bet.amount, 250)

    def test_display_hand(self):
        """ Test player can correctly display a hand """
        player = self._player
        self.assertEqual(player.display_hand(), 'Player John has [10] [A]')

    def test_dunder_str(self):
        """ Test player name and role are correctly displayed """
        player = self._player
        self.assertEqual(str(player), 'Player John')

    def test_hand(self):
        """ Test player has a hand """
        player = self._player
        for index, card in enumerate(player.hand):
            self.assertEqual(card, self._cards[index])

    def test_name(self):
        """ Test player has a name """
        player = self._player
        self.assertEqual(player.name, 'John')

    def test_role(self):
        """ Test player has a role """
        player = self._player
        self.assertEqual(player.role, 'Player')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
