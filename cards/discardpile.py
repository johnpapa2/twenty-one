"""
Created on Feb 3, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging


class DiscardPile():
    """ This is a class for a discard pile used in any card game.

    A discard pile from this class should work for any standard card game.

    """
    def __init__(self):
        """ Initialize the discard pile """
        self._cards = list()
        self._logger = logging.getLogger('bj')
        self._logger.info("New discard pile is empty.")

    def __getitem__(self, position):
        """ Return the card at a given position

        Arguments:
            position - The position of the card to return
        """
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the discard pile """
        return len(self._cards)

    def receives(self, card):
        """ Add a card to the discard pile

        Arguments:
            card - The card being discarded from a player's hand or the shoe
        """
        self._logger.debug(f"  Discarding a {card}")
        self._cards.append(card)
