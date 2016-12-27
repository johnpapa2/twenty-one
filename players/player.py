"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click
import logging

from cards.hand import Hand


class Player():

    def __init__(self, name, position='Player'):
        self._name = name
        self._position = position
        self._hand = Hand()
        self._busted = False
        self._wins = 0
        self._losses = 0
        self._logger = logging.getLogger('bj')
        if position == 'Dealer':
            self._logger.info(f"{self} taps into table")
        elif position == 'Player':
            self._logger.info(f"{self} sits at table")

    def __str__(self):
        return f"{self.position} {self.name}"

    @property
    def busted(self):
        return self._busted

    @busted.setter
    def busted(self, value):
        self._busted = value

    @property
    def hand(self):
        return self._hand

    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @property
    def total(self):
        self._logger.debug(f"{self} adds up hand")
        total = self.hand.value
        return total

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    def display_hand(self):
        ranks = [card.rank for card in self.hand]
        hand = '] ['.join(ranks)
        self._logger.info(f"{self} has [{hand}]")

    def doubles(self, card):
        self._logger.info(f"{self} doubles")
        self.receives(card)

    def hits(self, card):
        self._logger.info(f"{self} hits")
        self.receives(card)

    def init_hand(self):
        self._hand = Hand()

    def move(self, deck, dealers_hand):
        move = None

        if self.position == 'Player':
            self._logger.info(f"Dealer shows a [{dealers_hand[0].rank}]")
            self.display_hand()
            if self.total != 21:
                while move != 'stand':
                    move = click.prompt(f"Hand total {self.total}, Your Move", default='stand')
                    if move == 'hit':
                        self.hits(deck.deal_card())
                        self.display_hand()
                    elif move == 'double':
                        self.doubles(deck.deal_card())
                        self.display_hand()
                        break
                    if self.total > 21:
                        self.busted = True
                        self._logger.info(f"{self} Busted!")
                        break
                if move == 'stand':
                    self._logger.info(f"{self} stands!")
        else:
            self.display_hand()
            while self.total < 17:
                self.hits(deck.deal_card())
                self.display_hand()
                if self.total > 21:
                    self.busted = True
                    break

        self._logger.info(f"{self}'s hand value is {self.total}")

    def receives(self, card):
        self.hand.add_card(card)
        if self.position != 'Discard':
            self._logger.debug(f"{self} gets {card}")
