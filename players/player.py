"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 - 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click
import logging

from .bet import Bet
from .bankroll import Bankroll
from .bjhand import BjHand


class Player():

    def __init__(self, name, role='Player'):
        self._bet = Bet()
        self._bankroll = Bankroll(1000)
        self._hand = BjHand()
        self._name = name
        self._role = role
        self._logger = logging.getLogger('bj')
        if role == 'Dealer':
            self._logger.info(f"{self} taps into table")
        elif role == 'Player':
            self._logger.info(f"{self} sits at table")

    def __str__(self):
        return f"{self.role} {self.name}"

    @property
    def bankroll(self):
        return self._bankroll

    @property
    def bet(self):
        return self._bet

    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    @property
    def role(self):
        return self._role

    def display_hand(self):
        hand_display = f"{self} has {self.hand}"
        return hand_display

    def move(self, shoe, dealers_hand):
        move = None

        if self.role == 'Player':
            self._logger.info(f"Dealer shows a [{dealers_hand[0].rank}]")
            self._logger.info(self.display_hand())
            if self.total != 21:
                while move != 'stand':
                    move = click.prompt(f"Hand total {self.total}, Your Move", default='stand')
                    if move == 'hit':
                        self._logger.info(f"{self} hits")
                        self.receives(shoe.deal_card())
                        self._logger.info(self.display_hand())
                    elif move == 'double':
                        self._logger.info(f"{self} doubles")
                        self.bankroll -= self.hand.bet
                        self.hand.bet += self.hand.bet
                        self.receives(shoe.deal_card())
                        self._logger.info(self.display_hand())
                        break
                    if self.total > 21:
                        self.busted = True
                        self._logger.info(f"{self} Busted!")
                        break
                if move == 'stand':
                    self._logger.info(f"{self} stands!")
        else:
            self._logger.info(self.display_hand())
            while self.total < 17:
                self.receives(shoe.deal_card())
                self._logger.info(self.display_hand())
                if self.total > 21:
                    self.busted = True
                    break

        self._logger.info(f"{self}'s hand value is {self.total}")

    def place_bet(self, bet):
        self._logger.info(f"{self}'s bankroll is ${self.bankroll.amount}")
        self.bankroll.amount -= bet
        self.bet.amount = bet
        self._logger.info(f"{self} bets ${bet} dollars.")

    def receives(self, card):
        self.hand.add_card(card)
        if self.role != 'Discard':
            self._logger.debug(f"{self} gets {card}")
