"""
Created on Jan 15, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging
import random

from .bjcard import BjCard


class Shoe:
    """ This is a class for a Shoe composed of blackjack cards.

    A shoe from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, num_decks=1):
        """ Initialize shoe with n number of decks, with each deck in standard 52 card new deck order

        Arguments:
            num_decks - The number of decks in the shoe.
        """
        self._ranks = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']
        self._suits = ['spades', 'diamonds', 'clubs', 'hearts']
        self._cards = list()
        for deck in range(num_decks):
            # New decks of cards increase in rank from Ace (low) to King for two suits
            self._cards += [BjCard(suit, rank) for suit in self._suits for rank in self._ranks if suit in ['spades', 'diamonds']]
            # Then the ranks go in reverse for the other half of the deck
            self._cards += [BjCard(suit, rank) for suit in self._suits for rank in reversed(self._ranks) if suit in ['clubs', 'hearts']]
            self._logger = logging.getLogger('bj')
            self._logger.info("New deck of cards opened and spread")

    def __getitem__(self, position):
        """ Return the card at a given position

        Arguments:
            position - The position of the card to return
        """
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the shoe """
        return len(self._cards)

    def deal_card(self):
        """ Remove the top card from the shoe and return it """
        card = self._cards.pop(0)
        self._logger.debug(f"  Dealing a {card}")
        return card

    def shuffle(self):
        """ Shuffle the shoe """
        # TODO: Implement real shuffling algorithms to simulate how people actually shuffle
        #       This will be useful for shuffle tracking simulations
        random.shuffle(self._cards)
        self._logger.info("Now's a good time to take a break while I shuffle")
