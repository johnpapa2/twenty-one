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

    def __init__(self, name, role='Player'):
        self._name = name
        self._role = role
        self._hand = Hand()
        self._bankroll = 1000
        self._busted = False
        self._wins = 0
        self._losses = 0
        self._logger = logging.getLogger('bj')
        if role == 'Dealer':
            self._logger.info(f"{self} taps into table")
        elif role == 'Player':
            self._logger.info(f"{self} sits at table")

    @property
    def bankroll(self):
        return self._bankroll

    @bankroll.setter
    def bankroll(self, value):
        self._bankroll = value

    def __str__(self):
        return f"{self.role} {self.name}"

    @property
    def bet(self):
        return self.hand.bet

    @property
    def busted(self):
        return self._busted

    @busted.setter
    def busted(self, value):
        if not isinstance(value, bool):
            raise ValueError()
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
    def role(self):
        return self._role

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
        hand_display = f"{self} has {self.hand}"
        return hand_display

    def empty_hand(self):
        self._hand = Hand()

    def move(self, deck, dealers_hand):
        move = None

        if self.role == 'Player':
            self._logger.info(f"Dealer shows a [{dealers_hand[0].rank}]")
            self._logger.info(self.display_hand())
            if self.total != 21:
                while move != 'stand':
                    move = click.prompt(f"Hand total {self.total}, Your Move", default='stand')
                    if move == 'hit':
                        self._logger.info(f"{self} hits")
                        self.receives(deck.deal_card())
                        self._logger.info(self.display_hand())
                    elif move == 'double':
                        self._logger.info(f"{self} doubles")
                        self.bankroll -= self.hand.bet
                        self.hand.bet += self.hand.bet
                        self.receives(deck.deal_card())
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
                self.receives(deck.deal_card())
                self._logger.info(self.display_hand())
                if self.total > 21:
                    self.busted = True
                    break

        self._logger.info(f"{self}'s hand value is {self.total}")

    def place_bet(self):
        self._logger.info(f"{self}'s bankroll is ${self.bankroll}")
        bet = click.prompt(f"{self}, please place your bet", default=10)
        while self.bankroll - bet < 0:
            bet = click.prompt(f"{self}, please place your bet", default=10)
        self.bankroll -= bet
        self.hand.bet = bet
        self._logger.info(f"{self} bets ${bet} dollars.")

    def receives(self, card):
        self.hand.add_card(card)
        if self.role != 'Discard':
            self._logger.debug(f"{self} gets {card}")
