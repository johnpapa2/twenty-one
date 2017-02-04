"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from abc import ABCMeta, abstractmethod


class Hand(metaclass=ABCMeta):
    """ This is an Abstract Base Class for Hand objects.

    Hands from this class should work for any game played with a standard French Deck.

    """
    def __init__(self):
        """ Initialize the hand as an empty list of cards """
        self._cards = list()

    def __getitem__(self, position):
        """ Return the card at a given position

        Arguments:
            position - The position of the card to return
        """
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the hand """
        return len(self._cards)

    def __str__(self):
        """ Returns a description of the hand """
        ranks = [card.rank for card in self._cards]
        hand = '] ['.join(ranks)
        return (f"[{hand}]")

    def add_card(self, card):
        """ Add a card to the hand

        Arguments:
            card - The card to be added to the hand.
        """
        self._cards.append(card)

    def remove_card(self, position):
        """ Remove a card from the hand

        Arguments:
            position - The position of the card to be removed from the hand.
        """
        card = self[position]
        self._cards.remove(card)
        return card

    @abstractmethod
    def value(self):
        """ Return the value of the hand """
